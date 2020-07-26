import ROOT as r
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, SetOwnership, TVector3
import math, sys, optparse, array, copy, os
import gc, inspect
import numpy as np

import include.Canvas as Canvas


################################# GLOBAL VARIABLES DEFINITION ####################################

runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-1]:
    WORKPATH += level
    WORKPATH += '/'

print('runningfile: ' + runningfile)

##################################### FUNCTION DEFINITION ########################################

def getObject(filename, key):

    _f = r.TFile(filename)
    _h = _f.Get(key)
    _hcopy = copy.deepcopy(_h)
    _f.Close()

    return _hcopy



if __name__ == "__main__":


    gROOT.ProcessLine('.L ' + WORKPATH + 'include/tdrstyle.C')
    gROOT.SetBatch(1)
    print('WORKPATH: ' + WORKPATH)
    r.setTDRStyle()

    ###########################
    ####   Parser object   ####
    ###########################
    parser = optparse.OptionParser(usage='usage: %prog [opts] FilenameWithSamples', version='%prog 1.0')
    parser.add_option('-t', '--tag', action='store', type=str, dest='tag', default='', help='Output tag')
    (opts, args) = parser.parse_args()



    #####################################
    ####   Construct TEfficiencies   ####
    #####################################
    DY_recoDG_genMu_eta = getObject('plots_dummyDY_pt10/th1fs.root', 'recoDG_genMu_eta')
    DY_recoGM_genMu_eta = getObject('plots_dummyDY_pt10/th1fs.root', 'recoGM_genMu_eta')
    DY_total_genMu_eta = getObject('plots_dummyDY_pt10/th1fs.root', 'total_genMu_eta')

    DY_eff_GM_eta = r.TEfficiency(DY_recoGM_genMu_eta, DY_total_genMu_eta)
    DY_eff_GM_eta.SetTitle(';;')
    DY_eff_DG_eta = r.TEfficiency(DY_recoDG_genMu_eta, DY_total_genMu_eta)
    DY_eff_DG_eta.SetTitle(';'+DY_total_genMu_eta.GetXaxis().GetTitle()+'; Efficiency')

    DY_EFF_eta = Canvas.Canvas("DY_EFF_eta", 'png', 0.62, 0.81, 0.87, 0.9, 1) 
    DY_EFF_eta.addRate(DY_eff_DG_eta, 'AP', 'Displaced Global', 'p', r.kBlue+2, True, 0, marker = 24)
    DY_EFF_eta.addRate(DY_eff_GM_eta, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 1, marker = 24)
    DY_EFF_eta.addLatex(0.9, 0.93, 'Monte Carlo: DYJetsToLL_M-50', size = 0.032, align = 31)
    DY_EFF_eta.saveRatio(1, 0, 0, '', DY_eff_DG_eta, DY_eff_GM_eta, label = 'DG/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')



    if not os.path.exists(WORKPATH + 'harvested_'+opts.tag+'/'): os.makedirs(WORKPATH + 'harvested_'+opts.tag+'/')
