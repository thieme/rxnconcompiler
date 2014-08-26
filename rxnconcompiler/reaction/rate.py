#!/usr/bin/env python

"""
Module rate.py - containes Rate class.

---------------
Rates in rxncon:
---------------
Each Reaction in rxncon has a single Rate object
1. Basic Rate is created in ReactionFactory when creating a reaction.
2. Rate is updated in ComplexAplicator 
   (e.g. for K+/K- <bool> and for booleans that contain Input state).
3. Rate is updated in ContingencyAplicator 
   (for K+/K- contingencies and for contingencies with Input state).

------------------------------
Rates for AlternativeReactions.
------------------------------
(One reaction may happen in different circumstances)
A. All reactions that fullfill the coondition 
   defined by K+/K- have the same rate.
B. All reactions that don't fullfill the condition 
   defined by K+/K- have the same rate (different than in A).
C. For reactions with multiple K+/K- conditions the number of rates will grow.
   e.g. 
   Reaction first_K True, second_K True     k1_1
   Reaction first_K True, second_K False    k1_2  
   Reaction first_K False, second_K True    k1_3
   Reaction first_K False, second_K False   k1_4
D. Rates for reactions with input conditions contain functions.
   One Reaction may have two rates - when Input is present and when it is absent. 

------------------------------------
What the single Rate Object contains:
------------------------------------
A. Single rate/rates
   e.g. 
   k1
   k3_1
   kf1, kr1
   kf3_1, kr3_1
B. Function / functions:
   e.g.   

--------------
Rate functions:
--------------
A. Turns reaction on / off depending on Input presence:
   k1*k_Input
   k1*(1-k_Input)
B. Is a switch between two rates:
   k1_1*(1-k_Input)+k1_2*k_Input
We are not handling multiple Input conditions now.

--------------------------
How is the rate name built:
--------------------------
A. Normal rates:
   e.g. k3_5, kf1, kr1
   - rate letter 
     (k - irreversible reaction, kf - forward reaction, kr - reverse reaction)
   - reaction continer id (3)
   When there are more possible contexts for one reaction (more rates needed):
   - underscor
   - rate id (subrate) within main id
   Rate and reaction id don't need to be equal.
B. Input rates:
   e.g. k_start
   - rate letter (k)
   - underscor
   - Input name  
"""

import re

class Rate:
    """
    Object Rate keeps info about rates for a single reaction.

    Rate is set when reaction is created (in ReactionFactory).
    Basic reat is a simple one e.g. k1.
    Rate needs to get updated:
    - when applying complexes - boolean contingencies on reaction:
      --- when k+/k- <bool> (more rates, number of rates != number of rules!!!)
      --- when Input is a part of boolean (add a function)
    - when applying contingencies
      --- when k+/k- cont (more rates (*2), number of rates == number of rules)
      --- when Input is a part of contingency (add a function)

    We are not dealing with multiple input conditions for one reaction.
    """
    def __init__(self, reaction=None):
        # rate names
        self.rate = None # rate for irreversible reaction.
        self.frate = None # forward rate.
        self.rrate = None # reverse rate.
        # simple rate name can be exchanged with a functuin.
        # it allows to include conditions e.g. input.
        self._rate_names = [] # e.g. ['kf1_1', 'kr1_1'].
        self._special_rate_names = [] # e.g. ['k_start']

        if reaction:
            self.set_basic_rates(reaction)

    def __repr__(self):
        """"""
        return  str(self.get_rates_for_reaction())

    def set_basic_rates(self, reaction):
        """
        Sets rate names based on reaction data.

        Name can be a simple name (e.g. k1, kf1, kr1, k1_1) 
        or a function (we have three types of functions)
        
        For a reversible reaction frate and rrate have values and rate is None.
        For a irreversible reaction rate has a value and frate and frate are None.
        """
        if reaction.definition['Reversibility'] == 'irreversible':
            self.rate = 'k%s' % reaction.rid # rate for irreversible reaction
            self._rate_names = [self.rate]
        else:
            self.frate = 'kf%s' % reaction.rid # forward rate
            self.rrate = 'kr%s' % reaction.rid # reverse rate
            self._rate_names = [self.frate, self.rrate] # e.g. [kf1_1, kr1_1, k_start]

    def get_rates_for_reaction(self):
        """
        Returns rate names (or functions) as a list of strings.
        """
        if self.rate:
            return [self.rate]
        else:
            return [self.frate, self.rrate]

    def get_ids(self):
        """
        Returns ids used in this Rate object
        e.g. 
        [1_1, 1_2]
        [1]
        One Rate may hace maximaly two such ids.
        """
        rates = []
        for rate in self._rate_names:
            new_id = re.sub('kr|kf|k', '', rate)
            if new_id not in rates:
                rates.append(new_id)
        return rates

    def get_rate_values(self):
        """
        Returns dict:
        {Rate_name: rate_value}
        All normal rate values are set to 1.
        All special (input) rate values are set to 0
        """
        rates_dict = {}
        for rate in self._rate_names:
            rates_dict[rate] = 1
        for rate in self._special_rate_names:
            rates_dict[rate] = 0
        return rates_dict

    def update_name(self, new_num, new_num2=None):
        """
        Exchanges number after k in the rate name with given value. 
        E.g. 
        1_2 ---> self.rate = k1_2
        3_2 ---> self.frate = kf3_2 
        """
        if self.rate:
            new_rate = 'k%s' % new_num
            self.rate = self.rate.replace(self._rate_names[0], new_rate)
            self._rate_names[0] = new_rate
            # this part is for updating ones with two rates e.g. when K+ input
            if new_num2 and len(self._rate_names) > 1:
                new_rate = 'k%s' % new_num2
                self.rate = self.rate.replace(self._rate_names[1], new_rate)
                self._rate_names[1] = new_rate
        else:
            new_frate = 'kf%s' % new_num
            new_rrate =  'kr%s' % new_num
            self.frate = self.frate.replace(self._rate_names[0], new_frate)
            self.rrate = self.rrate.replace(self._rate_names[1], new_rrate)
            self._rate_names[0] = new_frate
            self._rate_names[1] = new_rrate
            # this part is for updating rates with two rates e.g. k+ input or ppi input
            if new_num2 and len(self._rate_names) > 2:
                new_frate = 'kf%s' % new_num2
                new_rrate =  'kr%s' % new_num2
                # only reverse reaction has two rates:
                if len(self._rate_names) == 3:
                    self.rrate = self.rrate.replace(self._rate_names[2], new_rrate)
                    self._rate_names[2] = new_rrate
                # both forward and reverse reactions have two rates:
                elif len(self._rate_names) == 4:
                    self.frate = self.frate.replace(self._rate_names[2], new_frate)
                    self.rrate = self.rrate.replace(self._rate_names[3], new_rrate)
                    self._rate_names[2] = new_frate
                    self._rate_names[3] = new_rrate

    def update_function(self, contingency, is_switch, num1, num2):
        """
        Exchanges rate number with function.
        """
        special = 'k_%s' % contingency.state.components[0].name
        self._special_rate_names = [special]
        if is_switch:
            if self.rate:
                self.rate = 'k%s*(1-%s)+k%s*%s' % (num2, special, num1, special)
                self._rate_names = ['k%s' % num1, 'k%s' % num2]
            else:
                self.frate = 'kf%s*(1-%s)+kf%s*%s' % (num2, special, num1, special)
                self.rrate = 'kr%s*(1-%s)+kr%s*%s' % (num2, special, num1, special)
                self._rate_names = ['kf%s' % num1, 'kr%s' % num1, 'kf%s' % num2, 'kr%s' % num2]
        else:
            if self.rate:    
                if contingency.ctype == 'x':
                    self.rate = 'k%s*(1-%s)' % (num1, special)
                elif contingency.ctype == '!':
                    self.rate = 'k%s*%s' % (num1, special)
                self._rate_names = ['k%s' % num1]       

            else:
                if contingency.ctype == 'x':
                    # reverse reaction always need two rates: dissociation even when input is not present.
                    self.frate = 'kf%s*(1-%s)' % (num2, special)
                    self.rrate = 'kr%s*(1-%s)+kr%s*%s' % (num2, special, num1, special)
                    self._rate_names = ['kf%s' % num1, 'kr%s' % num1, 'kr%s' % num2]
                elif contingency.ctype == '!':
                    # reverse reaction always need two rates: dissociation even when input is not present.
                    self.frate = 'kf%s*%s' % (num1, special)
                    self.rrate = 'kr%s*(1-%s)+kr%s*%s' % (num2, special, num1, special)
                self._rate_names = ['kf%s' % num1, 'kr%s' % num1, 'kr%s' % num2]