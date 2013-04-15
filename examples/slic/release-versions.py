###########################################
#
# iLCSoft versions for release v01-16
#
# F.Gaede, DESY 09.12.2011
#
###########################################


# --------- ilcsoft release version ------------------------------------------
ilcsoft_release='v01-17-01-pre'
# ----------------------------------------------------------------------------


# --------- install dir ------------------------------------------------------
ilcsoft_install_prefix = "/scratch/$USER/slic/"

#ilcsoft_install_prefix = ilcsoft_afs_path[ arch ]
#ilcsoft_install_prefix = "/scratch/gaede/ilcsoft/"
#ilcsoft_install_prefix = "/scratch/rosem/ilcsoft/"

#ilcsoft_install_dir = os.path.join( ilcsoft_install_prefix, ilcsoft_release )
# ----------------------------------------------------------------------------


# --------- ilcsoft home -----------------------------------------------------
# python variable for referring the ILC Home directory
# used to link or use already installed packages (SL4 or SL5)
# no need to set this variable if using SL4 or SL5 with access to /afs/desy.de/
#ilcPath = '/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6'
#ilcPath = '/afs/desy.de/project/ilcsoft/sw/x86_64_gcc41_sl5'
#ilcPath = ilcsoft_afs_path[ arch ]
#fg? ilcPath = ilcsoft_install_prefix
# ----------------------------------------------------------------------------

# ======================= PACKAGE VERSIONS ===================================

# xerces-c (needed by geant4 for building gdml support - required by mokka)
#XERCESC_ROOT_DIR = ilcPath + "/xercesc/2.7.0"

# ----- java ---------------------------------------------------------
Java_version = "1.6.0"
#Java_path = ilcPath + "/java/" + Java_version # comment out to try auto-detect
Java_path = "/usr/"

XercesC_version = "3.1.1" 

HepPDT_version = "3.04.01"

Geant4_version = "9.6.p01"

#ROOT_version = "5.34.05" 
#CLHEP_version = "2.1.3.1"

CMake_version = "2.8.5"

LCIO_version = "v02-03-03"

ILCUTIL_version = "v01-00"

#LCDD_version = "???"

