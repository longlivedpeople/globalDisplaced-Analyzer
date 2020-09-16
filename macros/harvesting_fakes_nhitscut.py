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
    """
    SI_fake_DG_dxy = getObject('fakes_signal_ptmin10_sigmapt0p4_chi3/th1fs.root', 'total_DG_dxy_clone')
    SI_fake_DG_dxy.SetTitle(';DG |d_{xy}| (cm);Fake rate')
    SI_fake_DG_dxy_ = Canvas.Canvas("SI_DG_dxy_nhitcut", 'png', 0.7, 0.73, 0.87, 0.88, 1)
    SI_fake_DG_dxy_.addRate(SI_fake_DG_dxy, 'AP', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'p', r.kBlue+2, True, 0, marker = 24)
    SI_fake_DG_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_nhitcut_'+opts.tag+'/')
    """

    # Check nhit fakes with binning and DY
    DY_fake_DG_nvalid = getObject('fakes_DY2M_ptmin31_sigmapt0p3_chi10/th1fs.root', 'total_DG_numberOfValidHits_clone')
    SI_fake_DG_nvalid_bin1 = getObject('fakes_signal_ptmin31_sigmapt0p3_chi10/th1fs.root', 'total_DG_numberOfValidHits_bin1_clone')
    SI_fake_DG_nvalid_bin2 = getObject('fakes_signal_ptmin31_sigmapt0p3_chi10/th1fs.root', 'total_DG_numberOfValidHits_bin2_clone')
    SI_fake_DG_nvalid_bin3 = getObject('fakes_signal_ptmin31_sigmapt0p3_chi10/th1fs.root', 'total_DG_numberOfValidHits_bin3_clone')
    DY_fake_DG_nvalid.SetTitle(';Numbes of valid hits N_{Hits};Fake rate')
    SI_fake_DG_nvalid_bin1.SetTitle(';;')
    SI_fake_DG_nvalid_bin2.SetTitle(';;')
    SI_fake_DG_nvalid_bin3.SetTitle(';;')
    SI_fake_DG_nvalid_bins_ = Canvas.Canvas("SI_fake_DG_nvalid_bins", 'png', 0.31, 0.73, 0.53, 0.88, 1)
    SI_fake_DG_nvalid_bins_.addRate(DY_fake_DG_nvalid, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed+2, True, 0, marker = 24)
    SI_fake_DG_nvalid_bins_.addRate(SI_fake_DG_nvalid_bin1, 'AP,SAME', 'H#rightarrowXX#rightarrow4l (All masses): |d_{xy}| < 1 cm', 'p', r.kBlue-9, True, 1, marker = 24)
    SI_fake_DG_nvalid_bins_.addRate(SI_fake_DG_nvalid_bin2, 'AP,SAME', 'H#rightarrowXX#rightarrow4l (All masses): 1 < |d_{xy}| < 20 cm', 'p', r.kBlue-4, True, 2, marker = 25)
    SI_fake_DG_nvalid_bins_.addRate(SI_fake_DG_nvalid_bin3, 'AP,SAME', 'H#rightarrowXX#rightarrow4l (All masses): |d_{xy}| > 20 cm', 'p', r.kBlack, True, 3, marker = 26)
    SI_fake_DG_nvalid_bins_.addLatex(0.4, 0.5, 'p_{T}^{DG} > 31 GeV, |#eta^{DG}| < 2', size = 0.03, align = 11)
    SI_fake_DG_nvalid_bins_.addLatex(0.4, 0.45, '#sigma_{p_{T}}/p_{T} < 0.3, #chi^{2}/ndof < 10', size = 0.03, align = 11)
    SI_fake_DG_nvalid_bins_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_nhitcut_'+opts.tag+'/')

    # bin1
    SI_matched_DG_nvalid = getObject('fakes_signal_ptmin31_sigmapt0p3_chi10/th1fs.root', 'matched_DG_numberOfValidHits_bin1')
    SI_unmatched_DG_nvalid = getObject('fakes_signal_ptmin31_sigmapt0p3_chi10/th1fs.root', 'unmatched_DG_numberOfValidHits_bin1')
    SI_DG_nvalid = doFakeStack(SI_matched_DG_nvalid, SI_unmatched_DG_nvalid)
    SI_DG_nvalid.SetMinimum(10)
    SI_DG_nvalid.SetMaximum(1e7)
    SI_DG_nvalid_ = Canvas.Canvas("SI_DG_nvalid_bin1", 'png', 0.52, 0.72, 0.87, 0.81, 1)
    SI_DG_nvalid_.addStack(SI_DG_nvalid, 'HIST', 1, 0)
    SI_DG_nvalid_.addLatex(0.17, 0.86, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 11)
    SI_DG_nvalid_.addLatex(0.17, 0.81, 'p_{T}^{DG} > 31 GeV, |#eta^{DG}| < 2', size = 0.03, align = 11)
    SI_DG_nvalid_.addLatex(0.17, 0.76, '#sigma_{p_{T}}/p_{T} < 0.3, #chi^{2}/ndof < 10', size = 0.03, align = 11)
    SI_DG_nvalid_.addLatex(0.17, 0.70, '|d_{xy}^{DG}| < 1 cm', size = 0.03, align = 11)
    SI_DG_nvalid_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_nhitcut_'+opts.tag+'/')

    # bin2
    SI_matched_DG_nvalid = getObject('fakes_signal_ptmin31_sigmapt0p3_chi10/th1fs.root', 'matched_DG_numberOfValidHits_bin2')
    SI_unmatched_DG_nvalid = getObject('fakes_signal_ptmin31_sigmapt0p3_chi10/th1fs.root', 'unmatched_DG_numberOfValidHits_bin2')
    SI_DG_nvalid = doFakeStack(SI_matched_DG_nvalid, SI_unmatched_DG_nvalid)
    SI_DG_nvalid.SetMinimum(1)
    SI_DG_nvalid.SetMaximum(5e6)
    SI_DG_nvalid_ = Canvas.Canvas("SI_DG_nvalid_bin2", 'png', 0.52, 0.72, 0.87, 0.81, 1)
    SI_DG_nvalid_.addStack(SI_DG_nvalid, 'HIST', 1, 0)
    SI_DG_nvalid_.addLatex(0.17, 0.86, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 11)
    SI_DG_nvalid_.addLatex(0.17, 0.81, 'p_{T}^{DG} > 31 GeV, |#eta^{DG}| < 2', size = 0.03, align = 11)
    SI_DG_nvalid_.addLatex(0.17, 0.76, '#sigma_{p_{T}}/p_{T} < 0.3, #chi^{2}/ndof < 10', size = 0.03, align = 11)
    SI_DG_nvalid_.addLatex(0.17, 0.70, '1 < |d_{xy}^{DG}| < 20 cm', size = 0.03, align = 11)
    SI_DG_nvalid_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_nhitcut_'+opts.tag+'/')

    # bin3
    SI_matched_DG_nvalid = getObject('fakes_signal_ptmin31_sigmapt0p3_chi10/th1fs.root', 'matched_DG_numberOfValidHits_bin3')
    SI_unmatched_DG_nvalid = getObject('fakes_signal_ptmin31_sigmapt0p3_chi10/th1fs.root', 'unmatched_DG_numberOfValidHits_bin3')
    SI_DG_nvalid = doFakeStack(SI_matched_DG_nvalid, SI_unmatched_DG_nvalid)
    SI_DG_nvalid.SetMinimum(1)
    SI_DG_nvalid.SetMaximum(5e6)
    SI_DG_nvalid_ = Canvas.Canvas("SI_DG_nvalid_bin3", 'png', 0.52, 0.72, 0.87, 0.81, 1)
    SI_DG_nvalid_.addStack(SI_DG_nvalid, 'HIST', 1, 0)
    SI_DG_nvalid_.addLatex(0.17, 0.86, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 11)
    SI_DG_nvalid_.addLatex(0.17, 0.81, 'p_{T}^{DG} > 31 GeV, |#eta^{DG}| < 2', size = 0.03, align = 11)
    SI_DG_nvalid_.addLatex(0.17, 0.76, '#sigma_{p_{T}}/p_{T} < 0.3, #chi^{2}/ndof < 10', size = 0.03, align = 11)
    SI_DG_nvalid_.addLatex(0.17, 0.70, '|d_{xy}^{DG}| > 20 cm', size = 0.03, align = 11)
    SI_DG_nvalid_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_nhitcut_'+opts.tag+'/')
