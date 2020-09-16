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

def makeOFHisto(h):

    """
    Function to make overflow histograms
       Parameter: Histogram
       Return:    Same histogram with an additional bin with events out of x axis
    """

    nbin = h.GetNbinsX()
    bw = h.GetBinWidth(1)
    xmin = h.GetXaxis().GetBinLowEdge(1)
    xmax = h.GetXaxis().GetBinUpEdge(nbin)
    _h = r.TH1F(h.GetName() + '_OF', '', nbin + 1, xmin, xmax + bw)

    for _bin in range(1, nbin + 2):
        _h.SetBinContent(_bin, h.GetBinContent(_bin))
        _h.SetBinError(_bin, h.GetBinError(_bin))

    _h.GetXaxis().SetTitle(h.GetXaxis().GetTitle())
    _h.GetYaxis().SetTitle(h.GetYaxis().GetTitle())

    return _h


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

    # Pt validation 
    passed_DG_pt_nocuts = getObject('qass_signal_eta2/th1fs.root', 'true_DG_pt') 
    passed_DG_pt_ID = getObject('qass_signal_eta2_sigmapt3p0_chi10_nhit22/th1fs.root', 'true_DG_pt') 
    total_DG_pt_nocuts = getObject('qass_signal_eta2/th1fs.root', 'total_DG_pt') 
    total_DG_pt_ID = getObject('qass_signal_eta2_sigmapt3p0_chi10_nhit22/th1fs.root', 'total_DG_pt') 
    SI_DG_pt_nocuts = r.TEfficiency(passed_DG_pt_nocuts, total_DG_pt_nocuts)
    SI_DG_pt_ID = r.TEfficiency(passed_DG_pt_ID, total_DG_pt_ID)
    SI_DG_pt_nocuts.SetTitle(';DG p_{T} (GeV);Charge assignment efficiency')
    SI_DG_pt_ID.SetTitle(';;')
    SI_DG_pt_ = Canvas.Canvas("SI_DG_pt", 'png', 0.4, 0.81, 0.6, 0.89, 1)
    SI_DG_pt_.addRate(SI_DG_pt_nocuts, 'AP', 'No cuts applied', 'p', r.kBlack, 1, 0, marker = 24)
    SI_DG_pt_.addRate(SI_DG_pt_ID, 'AP,SAME', '#sigma_{p_{T}}/p_{T} < 0.3, #chi^{2}/ndof < 10, N_{Hit} > 22', 'p', r.kBlue-4, 1, 1, marker = 24)
    SI_DG_pt_.addLatex(0.87, 0.17, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31, font = 62)
    SI_DG_pt_.addLatex(0.9, 0.93, '|#eta^{DG}| < 2', size = 0.03, align = 31)
    SI_DG_pt_.addLine(31, 0, 31, 1.2, r.kBlack, thickness = 1)
    SI_DG_pt_.save(1, 0, 0, '','', xlog = False, outputDir = WORKPATH + 'harvested_qass_'+opts.tag+'/')

    # sigmapt validation 
    passed_DG_sigmapt_nocuts = getObject('qass_signal_eta2/th1fs.root', 'true_DG_ptSig') 
    passed_DG_sigmapt_ID = getObject('qass_signal_eta2_ptmin31_chi10_nhit22/th1fs.root', 'true_DG_ptSig') 
    total_DG_sigmapt_nocuts = getObject('qass_signal_eta2/th1fs.root', 'total_DG_ptSig') 
    total_DG_sigmapt_ID = getObject('qass_signal_eta2_ptmin31_chi10_nhit22/th1fs.root', 'total_DG_ptSig') 
    SI_DG_sigmapt_nocuts = r.TEfficiency(passed_DG_sigmapt_nocuts, total_DG_sigmapt_nocuts)
    SI_DG_sigmapt_ID = r.TEfficiency(passed_DG_sigmapt_ID, total_DG_sigmapt_ID)
    SI_DG_sigmapt_nocuts.SetTitle(';DG #sigma_{p_{T}}/p_{T};Charge assignment efficiency')
    SI_DG_sigmapt_ID.SetTitle(';;')
    SI_DG_sigmapt_ = Canvas.Canvas("SI_DG_sigmapt", 'png', 0.34, 0.81, 0.6, 0.89, 1)
    SI_DG_sigmapt_.addRate(SI_DG_sigmapt_nocuts, 'AP', 'No cuts applied', 'p', r.kBlack, 1, 0, marker = 24)
    SI_DG_sigmapt_.addRate(SI_DG_sigmapt_ID, 'AP,SAME', 'p_{T} < 31 GeV, #chi^{2}/ndof < 10, N_{Hit} > 22', 'p', r.kBlue-4, 1, 1, marker = 24)
    SI_DG_sigmapt_.addLatex(0.87, 0.17, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31, font = 62)
    SI_DG_sigmapt_.addLatex(0.9, 0.93, '|#eta^{DG}| < 2', size = 0.03, align = 31)
    SI_DG_sigmapt_.addLine(0.3, 0, 0.3, 1.2, r.kBlack, thickness = 1)
    SI_DG_sigmapt_.save(1, 0, 0, '','', xlog = False, outputDir = WORKPATH + 'harvested_qass_'+opts.tag+'/')

    # chi2 validation 
    SI_DG_chi_nocuts = getObject('qass_signal_eta2/th1fs.root', 'qeff_DG_normChi2') 
    SI_DG_chi_ID = getObject('qass_signal_eta2_ptmin31_sigmapt3p0_nhit22/th1fs.root', 'qeff_DG_normChi2') 
    SI_DG_chi_nocuts.SetTitle(';DG #chi^{2}/ndof;Charge assignment efficiency')
    SI_DG_chi_ID.SetTitle(';;')
    SI_DG_chi_ = Canvas.Canvas("SI_DG_chi2", 'png', 0.11, 0.81, 0.48, 0.89, 1)
    SI_DG_chi_.addRate(SI_DG_chi_nocuts, 'AP', 'No cuts applied', 'p', r.kBlack, 1, 0, marker = 24)
    SI_DG_chi_.addRate(SI_DG_chi_ID, 'AP,SAME', 'p_{T} < 31 GeV, #sigma_{p_{T}}/p_{T} < 0.3, N_{Hit} > 22', 'p', r.kBlue-4, 1, 1, marker = 24)
    SI_DG_chi_.addLatex(0.15, 0.17, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 11, font = 62)
    SI_DG_chi_.addLatex(0.9, 0.93, '|#eta^{DG}| < 2', size = 0.03, align = 31)
    SI_DG_chi_.addLine(10, 0, 10, 1.2, r.kBlack, thickness = 1)
    SI_DG_chi_.save(1, 0, 0, '','', xlog = True, outputDir = WORKPATH + 'harvested_qass_'+opts.tag+'/')


    # nhit validation 
    passed_DG_numberOfValidHits_nocuts = getObject('qass_signal_eta2/th1fs.root', 'true_DG_numberOfValidHits') 
    passed_DG_numberOfValidHits_ID = getObject('qass_signal_eta2_ptmin31_sigmapt3p0_chi10/th1fs.root', 'true_DG_numberOfValidHits') 
    total_DG_numberOfValidHits_nocuts = getObject('qass_signal_eta2/th1fs.root', 'total_DG_numberOfValidHits') 
    total_DG_numberOfValidHits_ID = getObject('qass_signal_eta2_ptmin31_sigmapt3p0_chi10/th1fs.root', 'total_DG_numberOfValidHits') 
    SI_DG_numberOfValidHits_nocuts = r.TEfficiency(passed_DG_numberOfValidHits_nocuts, total_DG_numberOfValidHits_nocuts)
    SI_DG_numberOfValidHits_ID = r.TEfficiency(passed_DG_numberOfValidHits_ID, total_DG_numberOfValidHits_ID)
    SI_DG_numberOfValidHits_nocuts.SetTitle(';DG p_{T} (GeV);Charge assignment efficiency')
    SI_DG_numberOfValidHits_ID.SetTitle(';;')
    SI_DG_numberOfValidHits_ = Canvas.Canvas("SI_DG_numberOfValidHits", 'png', 0.35, 0.81, 0.6, 0.89, 1)
    SI_DG_numberOfValidHits_.addRate(SI_DG_numberOfValidHits_nocuts, 'AP', 'No cuts applied', 'p', r.kBlack, 1, 0, marker = 24)
    SI_DG_numberOfValidHits_.addRate(SI_DG_numberOfValidHits_ID, 'AP,SAME', 'p_{T} > 31 GeV, #sigma_{p_{T}}/p_{T} < 0.3, #chi^{2}/ndof < 10', 'p', r.kBlue-4, 1, 1, marker = 24)
    SI_DG_numberOfValidHits_.addLatex(0.87, 0.17, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31, font = 62)
    SI_DG_numberOfValidHits_.addLatex(0.9, 0.93, '|#eta^{DG}| < 2', size = 0.03, align = 31)
    SI_DG_numberOfValidHits_.addLine(22, 0, 22, 1.2, r.kBlack, thickness = 1)
    SI_DG_numberOfValidHits_.save(1, 0, 0, '','', xlog = False, outputDir = WORKPATH + 'harvested_qass_'+opts.tag+'/')


