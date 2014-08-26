=======================================================================
rxnconcompiler 
=======================================================================

rxnconcompiler is an iterative network building tool for Systems Biology.

Magdalena Rother, Sebastian Thieme, Ulrike Muenzner and Marcus Krantz

-----------------------------------------------------------------------

LEGAL DISCLAIMER

rxnconcompiler is released under the GPL license, a copy of which 
is included in the distribution (See COPYING for details). 

This software is provided "as-is". There are no expressed or implied 
warranties of any kind, including, but not limited to, the warranties of 
merchantability and fitness for a given application. In no event shall 
the authors be liable for any direct, indirect, incidental, special, 
exemplary or consequential damages (including, but not limited to, loss 
of use, data or profits, or business interruption) however caused and on 
any theory of liability, whether in contract, strict liability or tort 
(including negligence or otherwise) arising in any way out of the use 
of this software, even if advised of the possibility of such damage.

The authors take no responsibility for damage caused by this program 
or its components. 

-----------------------------------------------------------------------

CREDITS

Magdalena Rother   - architecture and unit tests and implementation
Sebastian Thieme   - model validation and testing
Ulrike Muenzner    - contribution into concepts
Marcus Krantz      - concept and supervision

-----------------------------------------------------------------------

ACKNOWLEDGEMENTS

Credit goes to our colleagues Falko Krause, Max Floettmann, 
David Jesinghaus, and Janina Linnik for their comments, 
ideas and support during development. 

-----------------------------------------------------------------------

REFERENCES

Magdalena Rother, Ulrike Muenzner, Sebastian Thieme and Marcus Krantz 

Information content and scalability in signal transduction 
network reconstruction formats. Molecular BioSystems, 
DOI: 10.1039/C3MB00005B (2013)

-----------------------------------------------------------------------

FOR DEVELOPERS

When using the repository version modify your ~/.bashrc :

PYTHONPATH=$PYTHONPATH:/path/to/main/rxnconcompiler/:
/path/to/rxnconcompiler/tests/
export PYTHONPATH

To be able to run acceptance tests with BioNetGen, 
install the BioNetGen software and add to ~/.bashrc :
BNG_PATH=/path/to/BioNetGen-2.2.2-stable/
export BNG_PATH