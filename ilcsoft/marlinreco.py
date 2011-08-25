##################################################
#
# MarlinReco module
#
# Author: Jan Engels, DESY
# Date: Jan, 2007
#
##################################################
                                                                                                                                                            
# custom imports
from marlinpkg import MarlinPKG

class MarlinReco(MarlinPKG):
    """ Responsible for the MarlinReco installation process. """
    
    def __init__(self, userInput):
        MarlinPKG.__init__(self, "MarlinReco", userInput )

        self.hasCMakeFindSupport = True

        # required modules
        self.reqmodules = [ "Marlin", "MarlinUtil", "CLHEP", "GEAR", "GSL", "LCIO" ]

        # optional modules
        self.optmodules = [ "CERNLIB", "AIDA" ]

    def preCheckDeps(self):
        MarlinPKG.preCheckDeps(self)

        if( self.mode == "install" ):

            fflag = str(self.envcmake.setdefault('MARLINRECO_FORTRAN','ON'))

            if fflag == 'ON' or fflag == '1':
                self.addDependency( ['CERNLIB'] )

