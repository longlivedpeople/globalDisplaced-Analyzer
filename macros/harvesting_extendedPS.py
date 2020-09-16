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

def doFakeStack(matched, unmatched, doOF = True, fakedown = False, ymin = False, ymax = False):

    matched = makeOFHisto(matched)
    unmatched = makeOFHisto(unmatched)

    matched.SetLineColor(r.kBlack)
    unmatched.SetLineColor(r.kBlack)
    unmatched.SetFillColorAlpha(r.kRed+1, 0.7)
    matched.SetFillColorAlpha(r.kGreen+2, 0.7)
    matched.SetTitle('True displaced global')
    unmatched.SetTitle('Fake displaced global')


    Stack = r.THStack("aux_stack", ";"+matched.GetXaxis().GetTitle()+";DG yield")

    if fakedown:
        Stack.Add(matched)    
        Stack.Add(unmatched)    
    else:
        Stack.Add(unmatched)    
        Stack.Add(matched)    

    return Stack


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

    # Extension to higher phase space:
    SI_extended = getObject('fakes_signal_ptmin10/th1fs.root', 'total_DG_eta')
    SI_reduced = getObject('fakes_signal_ptmin31/th1fs.root', 'total_DG_eta')
    SI_extended.SetTitle(';DG #eta; DG yield')
    SI_reduced.SetTitle(';;')
    SI_extended.SetLineWidth(2)
    SI_reduced.SetLineWidth(2)
    SI_extended.SetMaximum(1.3*SI_extended.GetMaximum())
    SI_PS = Canvas.Canvas("SI_phaseSpace", 'png', 0.45, 0.76, 0.8, 0.84, 1) 
    SI_PS.addHisto(SI_extended, 'HIST', 'p_{T}^{DG} > 10 GeV, |#eta^{DG}| < 2.4', 'l', r.kRed-4, 1, 0)
    SI_PS.addHisto(SI_reduced, 'HIST, SAME', 'p_{T}^{DG} > 31 GeV, |#eta^{DG}| < 2', 'l', r.kBlue+2, 1, 1)
    SI_PS.addLatex(0.87, 0.86, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31, font = 62)
    SI_PS.save(1, 0, 0, '', '', outputDir = WORKPATH + 'harvested_PS_' + opts.tag+ '/', maxYnumbers = 3)

    #

    # Fake rate vs chi2 (2 spaces)
    SI_fake_DG_chi_max = getObject('fakes_signal_ptmin10_sigmapt0p3/th1fs.root', 'pfake_DG_normChi2')
    SI_fake_DG_chi_min = getObject('fakes_signal_ptmin31_sigmapt0p3/th1fs.root', 'pfake_DG_normChi2')
    SI_fake_DG_chi_max.SetTitle(';DG #chi^{2}/ndof;DG Fake rate')
    SI_fake_DG_chi_min.SetTitle(';;')
    SI_fake_DG_chi_ = Canvas.Canvas("SI_fake_chicomp", 'png', 0.36, 0.76, 0.55, 0.84, 1)
    SI_fake_DG_chi_.addRate(SI_fake_DG_chi_max, 'AP', 'p_{T} > 10 GeV, |#eta^{DG}| < 2.4, #sigma_{p_{T}}/p_{T} < 0.3', 'p', r.kRed+2, True, 0, marker = 24)
    SI_fake_DG_chi_.addRate(SI_fake_DG_chi_min, 'AP, SAME', 'p_{T} > 31 GeV, |#eta^{DG}| < 2, #sigma_{p_{T}}/p_{T} < 0.3', 'p', r.kBlue+2, True, 1, marker = 24)
    SI_fake_DG_chi_.addLatex(0.87, 0.86, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31, font = 62)
    SI_fake_DG_chi_.save(1, 0, 0, '','', xlog = True, outputDir = WORKPATH + 'harvested_PS_'+opts.tag+'/')

    # Fake rate vs nhit (2 spaces)
    SI_fake_DG_nhit_max = getObject('fakes_signal_ptmin10_sigmapt0p3_chi3/th1fs.root', 'total_DG_numberOfValidHits_clone')
    SI_fake_DG_nhit_min = getObject('fakes_signal_ptmin31_sigmapt0p3_chi10/th1fs.root', 'total_DG_numberOfValidHits_clone')
    SI_fake_DG_nhit_max.SetTitle(';DG N_{Hit};DG Fake rate')
    SI_fake_DG_nhit_min.SetTitle(';;')
    SI_fake_DG_nhit_ = Canvas.Canvas("SI_fake_nhitcomp", 'png', 0.25, 0.76, 0.55, 0.84, 1)
    SI_fake_DG_nhit_.addRate(SI_fake_DG_nhit_max, 'AP', 'p_{T} > 10 GeV, |#eta^{DG}| < 2.4, #sigma_{p_{T}}/p_{T} < 0.3, #chi^{2}/ndof < 3', 'p', r.kRed+2, True, 0, marker = 24)
    SI_fake_DG_nhit_.addRate(SI_fake_DG_nhit_min, 'AP, SAME', 'p_{T} > 31 GeV, |#eta^{DG}| < 2, #sigma_{p_{T}}/p_{T} < 0.3, #chi^{2}/ndof < 10', 'p', r.kBlue+2, True, 1, marker = 24)
    SI_fake_DG_nhit_.addLatex(0.87, 0.86, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31, font = 62)
    SI_fake_DG_nhit_.save(1, 0, 0, '','', xlog = False, outputDir = WORKPATH + 'harvested_PS_'+opts.tag+'/')

    # Fake rate vs eta (2 spaces)
    SI_fake_DG_eta_max = getObject('fakes_signal_eta2p4/th1fs.root', 'total_DG_eta_clone')
    SI_fake_DG_eta_1 = getObject('fakes_signal_ptmin10/th1fs.root', 'total_DG_eta_clone')
    SI_fake_DG_eta_2 = getObject('fakes_signal_ptmin31/th1fs.root', 'total_DG_eta_clone')
    SI_fake_DG_eta_max.SetTitle(';DG #eta;DG Fake rate')
    SI_fake_DG_eta_1.SetTitle(';;')
    SI_fake_DG_eta_2.SetTitle(';;')
    #SI_fake_DG_eta_max.SetMaximum(5.0)
    SI_fake_DG_eta_ = Canvas.Canvas("SI_fake_eta", 'png', 0.35, 0.72, 0.55, 0.84, 1)
    SI_fake_DG_eta_.addRate(SI_fake_DG_eta_max, 'AP', '|#eta^{DG}| < 2.4', 'p', r.kBlack, True, 0, marker = 24)
    SI_fake_DG_eta_.addRate(SI_fake_DG_eta_1, 'AP, SAME', '|#eta^{DG}| < 2.4, p_{T}^{DG} > 10 GeV', 'p', r.kRed+2, True, 1, marker = 24)
    SI_fake_DG_eta_.addRate(SI_fake_DG_eta_2, 'AP, SAME', '|#eta^{DG}| < 2, p_{T}^{DG} > 31 GeV', 'p', r.kBlue+2, True, 1, marker = 24)
    SI_fake_DG_eta_.addLatex(0.87, 0.86, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31, font = 62)
    SI_fake_DG_eta_.save(1, 0, 1, '','', xlog = False, outputDir = WORKPATH + 'harvested_PS_'+opts.tag+'/')

    """
    # pT spectra in signal in stacked histogram
    SI_matched_DG_pt = getObject('fakes_signal_nocut_eta2/th1fs.root', 'matched_DG_pt')
    SI_unmatched_DG_pt = getObject('fakes_signal_nocut_eta2/th1fs.root', 'unmatched_DG_pt')
    SI_matched_DG_pt.SetTitle(';Reconstructed DG p_{T} (GeV);')
    SI_DG_pt = doFakeStack(SI_matched_DG_pt, SI_unmatched_DG_pt, fakedown = True)
    SI_DG_pt_ = Canvas.Canvas("SI_DG_pt_stacked_eta2", 'png', 0.52, 0.81, 0.87, 0.9, 1) 
    SI_DG_pt_.addStack(SI_DG_pt, 'HIST', 1, 0)
    SI_DG_pt_.addLatex(0.41, 0.75, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 11, font = 62)
    SI_DG_pt_.addLatex(0.41, 0.71, '|#eta^{DG}| < 2', size = 0.03, align = 11)
    SI_DG_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', maxYnumbers = 4)

    # Fake rate vs pT (signal and background)
    SI_fake_DG_pt = getObject('fakes_signal_nocut_eta2/th1fs.root', 'total_DG_pt_clone')
    DY_fake_DG_pt = getObject('fakes_DY2M_nocut_eta2/th1fs.root', 'total_DG_pt_clone')
    SI_fake_DG_pt.SetTitle(';DG p_{T} (GeV);DG Fake rate')
    DY_fake_DG_pt.SetTitle(';;')
    SI_fake_DG_pt_ = Canvas.Canvas("SI_fake_DG_pt_nocuts_eta2", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    SI_fake_DG_pt_.addRate(DY_fake_DG_pt, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed+2, True, 0, marker = 24)
    SI_fake_DG_pt_.addRate(SI_fake_DG_pt, 'AP, SAME', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'p', r.kBlue+2, True, 1, marker = 24)
    SI_fake_DG_pt_.addLatex(0.9, 0.93, '|#eta^{DG}| < 2|', size = 0.03, align = 31)
    SI_fake_DG_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/')
    """



