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
    """
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
    """

    ########################################

    
    SI_recoDG_genMu_Lxy = getObject('plots_signal/th1fs.root', 'recoDG_genMu_Lxy')
    SI_recoDGID_genMu_Lxy = getObject('plots_signal/th1fs.root', 'recoDGID_genMu_Lxy')
    SI_recoGM_genMu_Lxy = getObject('plots_signal/th1fs.root', 'recoGM_genMu_Lxy')
    SI_total_genMu_Lxy = getObject('plots_signal/th1fs.root', 'total_genMu_Lxy')
    SI_recoDG_genMu_Lxy.Rebin(2)
    SI_recoDGID_genMu_Lxy.Rebin(2)
    SI_recoGM_genMu_Lxy.Rebin(2)
    SI_total_genMu_Lxy.Rebin(2)

    SI_eff_GM_Lxy = r.TEfficiency(SI_recoGM_genMu_Lxy, SI_total_genMu_Lxy)
    SI_eff_GM_Lxy.SetTitle(';;')
    SI_eff_DG_Lxy = r.TEfficiency(SI_recoDG_genMu_Lxy, SI_total_genMu_Lxy)
    SI_eff_DG_Lxy.SetTitle(';'+SI_total_genMu_Lxy.GetXaxis().GetTitle()+'; Efficiency')
    SI_eff_DGID_Lxy = r.TEfficiency(SI_recoDGID_genMu_Lxy, SI_total_genMu_Lxy)
    SI_eff_DGID_Lxy.SetTitle(';'+SI_total_genMu_Lxy.GetXaxis().GetTitle()+'; Efficiency')

    SI_EFF_Lxy = Canvas.Canvas("SI_EFF_Lxy", 'png', 0.55, 0.78, 0.85, 0.9, 1) 
    SI_EFF_Lxy.addRate(SI_eff_DG_Lxy, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_Lxy.addRate(SI_eff_DGID_Lxy, 'AP, SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_Lxy.addRate(SI_eff_GM_Lxy, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_Lxy.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_Lxy.saveRatio(1, 0, 0, '', SI_eff_DGID_Lxy, SI_eff_GM_Lxy, r_ymin = 0.0, r_ymax = 4, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')
    
    ########################################

    SI_recoDG_genMu_dxy = getObject('plots_signal/th1fs.root', 'recoDG_genMu_dxy')
    SI_recoDGID_genMu_dxy = getObject('plots_signal/th1fs.root', 'recoDGID_genMu_dxy')
    SI_recoGM_genMu_dxy = getObject('plots_signal/th1fs.root', 'recoGM_genMu_dxy')
    SI_total_genMu_dxy = getObject('plots_signal/th1fs.root', 'total_genMu_dxy')
    SI_recoDG_genMu_dxy.Rebin(2)
    SI_recoDGID_genMu_dxy.Rebin(2)
    SI_recoGM_genMu_dxy.Rebin(2)
    SI_total_genMu_dxy.Rebin(2)

    SI_eff_GM_dxy = r.TEfficiency(SI_recoGM_genMu_dxy, SI_total_genMu_dxy)
    SI_eff_GM_dxy.SetTitle(';;')
    SI_eff_DG_dxy = r.TEfficiency(SI_recoDG_genMu_dxy, SI_total_genMu_dxy)
    SI_eff_DG_dxy.SetTitle(';'+SI_total_genMu_dxy.GetXaxis().GetTitle()+'; Efficiency')
    SI_eff_DGID_dxy = r.TEfficiency(SI_recoDGID_genMu_dxy, SI_total_genMu_dxy)
    SI_eff_DGID_dxy.SetTitle(';'+SI_total_genMu_dxy.GetXaxis().GetTitle()+'; Efficiency')

    SI_EFF_dxy = Canvas.Canvas("SI_EFF_dxy", 'png', 0.55, 0.78, 0.85, 0.9, 1) 
    SI_EFF_dxy.addRate(SI_eff_DG_dxy, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_dxy.addRate(SI_eff_DGID_dxy, 'AP, SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_dxy.addRate(SI_eff_GM_dxy, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_dxy.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_dxy.saveRatio(1, 0, 0, '', SI_eff_DGID_dxy, SI_eff_GM_dxy, r_ymin = 0.0, r_ymax = 10, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')

    ########################################
    
    SI_eff_GM_pt_Lxybin1 = getObject('plots_signal/th1fs.root', 'eff_GM_pt_Lxybin1')
    SI_eff_DG_pt_Lxybin1 = getObject('plots_signal/th1fs.root', 'eff_DG_pt_Lxybin1')
    SI_eff_DGID_pt_Lxybin1 = getObject('plots_signal/th1fs.root', 'eff_DGID_pt_Lxybin1')

    SI_EFF_pt_Lxybin1 = Canvas.Canvas("SI_EFF_pt_Lxybin1", 'png', 0.55, 0.78, 0.87, 0.9, 1) 
    SI_EFF_pt_Lxybin1.addRate(SI_eff_DG_pt_Lxybin1, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_pt_Lxybin1.addRate(SI_eff_DGID_pt_Lxybin1, 'AP,SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_pt_Lxybin1.addRate(SI_eff_GM_pt_Lxybin1, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_pt_Lxybin1.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_pt_Lxybin1.saveRatio(1, 0, 0, '', SI_eff_DGID_pt_Lxybin1, SI_eff_GM_pt_Lxybin1, r_ymin = 0.75, r_ymax = 1.25, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')

    ########################################

    SI_eff_GM_pt_Lxybin2 = getObject('plots_signal/th1fs.root', 'eff_GM_pt_Lxybin2')
    SI_eff_DG_pt_Lxybin2 = getObject('plots_signal/th1fs.root', 'eff_DG_pt_Lxybin2')
    SI_eff_DGID_pt_Lxybin2 = getObject('plots_signal/th1fs.root', 'eff_DGID_pt_Lxybin2')

    SI_EFF_pt_Lxybin2 = Canvas.Canvas("SI_EFF_pt_Lxybin2", 'png', 0.55, 0.78, 0.87, 0.9, 1) 
    SI_EFF_pt_Lxybin2.addRate(SI_eff_DG_pt_Lxybin2, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_pt_Lxybin2.addRate(SI_eff_DGID_pt_Lxybin2, 'AP,SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_pt_Lxybin2.addRate(SI_eff_GM_pt_Lxybin2, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_pt_Lxybin2.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_pt_Lxybin2.saveRatio(1, 0, 0, '', SI_eff_DGID_pt_Lxybin2, SI_eff_GM_pt_Lxybin2, r_ymin = 0.75, r_ymax = 1.25, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')

    ########################################

    SI_eff_GM_pt_Lxybin3 = getObject('plots_signal/th1fs.root', 'eff_GM_pt_Lxybin3')
    SI_eff_DG_pt_Lxybin3 = getObject('plots_signal/th1fs.root', 'eff_DG_pt_Lxybin3')
    SI_eff_DGID_pt_Lxybin3 = getObject('plots_signal/th1fs.root', 'eff_DGID_pt_Lxybin3')

    SI_EFF_pt_Lxybin3 = Canvas.Canvas("SI_EFF_pt_Lxybin3", 'png', 0.55, 0.78, 0.87, 0.9, 1) 
    SI_EFF_pt_Lxybin3.addRate(SI_eff_DG_pt_Lxybin3, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_pt_Lxybin3.addRate(SI_eff_DGID_pt_Lxybin3, 'AP,SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_pt_Lxybin3.addRate(SI_eff_GM_pt_Lxybin3, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_pt_Lxybin3.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_pt_Lxybin3.saveRatio(1, 0, 0, '', SI_eff_DGID_pt_Lxybin3, SI_eff_GM_pt_Lxybin3, r_ymin = 1.0, r_ymax = 3, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')

    
    ########################################

    SI_eff_GM_pt_Lxybin4 = getObject('plots_signal/th1fs.root', 'eff_GM_pt_Lxybin4')
    SI_eff_DG_pt_Lxybin4 = getObject('plots_signal/th1fs.root', 'eff_DG_pt_Lxybin4')
    SI_eff_DGID_pt_Lxybin4 = getObject('plots_signal/th1fs.root', 'eff_DGID_pt_Lxybin4')

    SI_EFF_pt_Lxybin4 = Canvas.Canvas("SI_EFF_pt_Lxybin4", 'png', 0.55, 0.78, 0.87, 0.9, 1) 
    SI_EFF_pt_Lxybin4.addRate(SI_eff_DG_pt_Lxybin4, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_pt_Lxybin4.addRate(SI_eff_DGID_pt_Lxybin4, 'AP,SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_pt_Lxybin4.addRate(SI_eff_GM_pt_Lxybin4, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_pt_Lxybin4.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_pt_Lxybin4.saveRatio(1, 0, 0, '', SI_eff_DGID_pt_Lxybin4, SI_eff_GM_pt_Lxybin4, r_ymin = 0.5, r_ymax = 3, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')


    ########################################

    SI_eff_GM_pt_dxybin1 = getObject('plots_signal/th1fs.root', 'eff_GM_pt_dxybin1')
    SI_eff_DG_pt_dxybin1 = getObject('plots_signal/th1fs.root', 'eff_DG_pt_dxybin1')
    SI_eff_DGID_pt_dxybin1 = getObject('plots_signal/th1fs.root', 'eff_DGID_pt_dxybin1')

    SI_EFF_pt_dxybin1 = Canvas.Canvas("SI_EFF_pt_dxybin1", 'png', 0.55, 0.78, 0.87, 0.9, 1) 
    SI_EFF_pt_dxybin1.addRate(SI_eff_DG_pt_dxybin1, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_pt_dxybin1.addRate(SI_eff_DGID_pt_dxybin1, 'AP,SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_pt_dxybin1.addRate(SI_eff_GM_pt_dxybin1, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_pt_dxybin1.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_pt_dxybin1.saveRatio(1, 0, 0, '', SI_eff_DGID_pt_dxybin1, SI_eff_GM_pt_dxybin1, r_ymin = 0.75, r_ymax = 1.25, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')

    ########################################

    SI_eff_GM_pt_dxybin2 = getObject('plots_signal/th1fs.root', 'eff_GM_pt_dxybin2')
    SI_eff_DG_pt_dxybin2 = getObject('plots_signal/th1fs.root', 'eff_DG_pt_dxybin2')
    SI_eff_DGID_pt_dxybin2 = getObject('plots_signal/th1fs.root', 'eff_DGID_pt_dxybin2')

    SI_EFF_pt_dxybin2 = Canvas.Canvas("SI_EFF_pt_dxybin2", 'png', 0.55, 0.78, 0.87, 0.9, 1) 
    SI_EFF_pt_dxybin2.addRate(SI_eff_DG_pt_dxybin2, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_pt_dxybin2.addRate(SI_eff_DGID_pt_dxybin2, 'AP,SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_pt_dxybin2.addRate(SI_eff_GM_pt_dxybin2, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_pt_dxybin2.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_pt_dxybin2.saveRatio(1, 0, 0, '', SI_eff_DGID_pt_dxybin2, SI_eff_GM_pt_dxybin2, r_ymin = 0.75, r_ymax = 1.5, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')

    ########################################

    SI_eff_GM_pt_dxybin3 = getObject('plots_signal/th1fs.root', 'eff_GM_pt_dxybin3')
    SI_eff_DG_pt_dxybin3 = getObject('plots_signal/th1fs.root', 'eff_DG_pt_dxybin3')
    SI_eff_DGID_pt_dxybin3 = getObject('plots_signal/th1fs.root', 'eff_DGID_pt_dxybin3')

    SI_EFF_pt_dxybin3 = Canvas.Canvas("SI_EFF_pt_dxybin3", 'png', 0.55, 0.78, 0.87, 0.9, 1) 
    SI_EFF_pt_dxybin3.addRate(SI_eff_DG_pt_dxybin3, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_pt_dxybin3.addRate(SI_eff_DGID_pt_dxybin3, 'AP,SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_pt_dxybin3.addRate(SI_eff_GM_pt_dxybin3, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_pt_dxybin3.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_pt_dxybin3.saveRatio(1, 0, 0, '', SI_eff_DGID_pt_dxybin3, SI_eff_GM_pt_dxybin3, r_ymin = 1, r_ymax = 10, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')

    
    ########################################

    SI_eff_GM_pt_dxybin4 = getObject('plots_signal/th1fs.root', 'eff_GM_pt_dxybin4')
    SI_eff_DG_pt_dxybin4 = getObject('plots_signal/th1fs.root', 'eff_DG_pt_dxybin4')
    SI_eff_DGID_pt_dxybin4 = getObject('plots_signal/th1fs.root', 'eff_DGID_pt_dxybin4')

    SI_EFF_pt_dxybin4 = Canvas.Canvas("SI_EFF_pt_dxybin4", 'png', 0.55, 0.78, 0.87, 0.9, 1) 
    SI_EFF_pt_dxybin4.addRate(SI_eff_DG_pt_dxybin4, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_pt_dxybin4.addRate(SI_eff_DGID_pt_dxybin4, 'AP,SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_pt_dxybin4.addRate(SI_eff_GM_pt_dxybin4, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_pt_dxybin4.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_pt_dxybin4.saveRatio(1, 0, 0, '', SI_eff_DGID_pt_dxybin4, SI_eff_GM_pt_dxybin4, r_ymin = 0.5, r_ymax = 1.5, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')



    ########################################

    SI_recoDGID_genMu_Lz = getObject('plots_signal/th1fs.root', 'recoDGID_genMu_Lz')
    SI_recoDG_genMu_Lz = getObject('plots_signal/th1fs.root', 'recoDG_genMu_Lz')
    SI_recoGM_genMu_Lz = getObject('plots_signal/th1fs.root', 'recoGM_genMu_Lz')
    SI_total_genMu_Lz = getObject('plots_signal/th1fs.root', 'total_genMu_Lz')
    SI_recoDGID_genMu_Lz.Rebin(2)
    SI_recoDG_genMu_Lz.Rebin(2)
    SI_recoGM_genMu_Lz.Rebin(2)
    SI_total_genMu_Lz.Rebin(2)

    SI_eff_GM_Lz = r.TEfficiency(SI_recoGM_genMu_Lz, SI_total_genMu_Lz)
    SI_eff_GM_Lz.SetTitle(';;')
    SI_eff_DG_Lz = r.TEfficiency(SI_recoDG_genMu_Lz, SI_total_genMu_Lz)
    SI_eff_DG_Lz.SetTitle(';'+SI_total_genMu_Lz.GetXaxis().GetTitle()+'; Efficiency')
    SI_eff_DGID_Lz = r.TEfficiency(SI_recoDGID_genMu_Lz, SI_total_genMu_Lz)
    SI_eff_DGID_Lz.SetTitle(';; Efficiency')

    SI_EFF_Lz = Canvas.Canvas("SI_EFF_Lz", 'png', 0.55, 0.78, 0.85, 0.9, 1) 
    SI_EFF_Lz.addRate(SI_eff_DG_Lz, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_Lz.addRate(SI_eff_DGID_Lz, 'AP,SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_Lz.addRate(SI_eff_GM_Lz, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_Lz.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_Lz.saveRatio(1, 0, 0, '', SI_eff_DGID_Lz, SI_eff_GM_Lz, r_ymin = 0.0, r_ymax = 8, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')

    ########################################

    SI_recoDGID_genMu_dz = getObject('plots_signal/th1fs.root', 'recoDGID_genMu_dz')
    SI_recoDG_genMu_dz = getObject('plots_signal/th1fs.root', 'recoDG_genMu_dz')
    SI_recoGM_genMu_dz = getObject('plots_signal/th1fs.root', 'recoGM_genMu_dz')
    SI_total_genMu_dz = getObject('plots_signal/th1fs.root', 'total_genMu_dz')
    SI_recoDGID_genMu_dz.Rebin(2)
    SI_recoDG_genMu_dz.Rebin(2)
    SI_recoGM_genMu_dz.Rebin(2)
    SI_total_genMu_dz.Rebin(2)

    SI_eff_GM_dz = r.TEfficiency(SI_recoGM_genMu_dz, SI_total_genMu_dz)
    SI_eff_GM_dz.SetTitle(';;')
    SI_eff_DG_dz = r.TEfficiency(SI_recoDG_genMu_dz, SI_total_genMu_dz)
    SI_eff_DG_dz.SetTitle(';'+SI_total_genMu_dz.GetXaxis().GetTitle()+'; Efficiency')
    SI_eff_DGID_dz = r.TEfficiency(SI_recoDGID_genMu_dz, SI_total_genMu_dz)
    SI_eff_DGID_dz.SetTitle(';; Efficiency')

    SI_EFF_dz = Canvas.Canvas("SI_EFF_dz", 'png', 0.55, 0.78, 0.85, 0.9, 1) 
    SI_EFF_dz.addRate(SI_eff_DG_dz, 'AP', 'Displaced Global', 'p', r.kBlack, True, 0, marker = 24)
    SI_EFF_dz.addRate(SI_eff_DGID_dz, 'AP,SAME', 'Displaced Global + ID', 'p', r.kBlue+1, True, 1, marker = 24)
    SI_EFF_dz.addRate(SI_eff_GM_dz, 'AP, SAME', 'Standard Global', 'p', r.kRed-7, True, 2, marker = 24)
    SI_EFF_dz.addLatex(0.9, 0.93, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.032, align = 31)
    SI_EFF_dz.saveRatio(1, 0, 0, '', SI_eff_DGID_dz, SI_eff_GM_dz, r_ymin = 0.0, r_ymax = 8, label = 'DG(+ID)/GM', outputDir = WORKPATH + 'harvested_'+opts.tag+'/')






    #if not os.path.exists(WORKPATH + 'harvested_'+opts.tag+'/'): os.makedirs(WORKPATH + 'harvested_'+opts.tag+'/')
