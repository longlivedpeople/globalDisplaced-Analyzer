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

    # Differences in pt
    BCK_unmatched_DG_pt = getObject('fakes_DY2M_nocut_eta2/th1fs.root', 'unmatched_DG_pt')
    SI_unmatched_DG_pt = getObject('fakes_signal_nocut_eta2/th1fs.root', 'unmatched_DG_pt')
    BCK_unmatched_DG_pt.Scale(1.0/BCK_unmatched_DG_pt.Integral())
    SI_unmatched_DG_pt.Scale(1.0/SI_unmatched_DG_pt.Integral())
    BCK_unmatched_DG_pt.SetLineWidth(2)
    SI_unmatched_DG_pt.SetLineWidth(2)
    BCK_unmatched_DG_pt.SetTitle(';Fake DG p_{T} (GeV);Normalized fake DG yield')
    SI_unmatched_DG_pt.SetTitle('')
    SI_DG_pt_ = Canvas.Canvas("unmatched_comp_pt", 'png', 0.35, 0.77, 0.67, 0.86, 1) 
    SI_DG_pt_.addHisto(BCK_unmatched_DG_pt, 'HIST', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'l', r.kRed+2, 1, 0)
    SI_DG_pt_.addHisto(SI_unmatched_DG_pt, 'HIST,SAME', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'l', r.kBlue+2, 1, 1)
    SI_DG_pt_.addLatex(0.9, 0.93, 'Displaced Global Muons: |#eta^{DG}| < 2', size = 0.04, align = 31)
    SI_DG_pt_.saveRatio(1, 0, 1, '', SI_unmatched_DG_pt, BCK_unmatched_DG_pt, r_ymin=0, r_ymax=10, label ="Sig/Bkg", outputDir = 'harvested_diffs/')


    BCK_matched_DG_pt = getObject('fakes_DY2M_nocut_eta2/th1fs.root', 'matched_DG_pt')
    SI_matched_DG_pt = getObject('fakes_signal_nocut_eta2/th1fs.root', 'matched_DG_pt')
    BCK_matched_DG_pt.Scale(1.0/BCK_matched_DG_pt.Integral())
    SI_matched_DG_pt.Scale(1.0/SI_matched_DG_pt.Integral())
    BCK_matched_DG_pt.SetLineWidth(2)
    SI_matched_DG_pt.SetLineWidth(2)
    BCK_matched_DG_pt.SetTitle(';True DG p_{T} (GeV);Normalized true DG yield')
    SI_matched_DG_pt.SetTitle('')
    SI_DG_pt_ = Canvas.Canvas("matched_comp_pt", 'png', 0.35, 0.77, 0.67, 0.86, 1) 
    SI_DG_pt_.addHisto(BCK_matched_DG_pt, 'HIST', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'l', r.kRed+2, 1, 0)
    SI_DG_pt_.addHisto(SI_matched_DG_pt, 'HIST,SAME', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'l', r.kBlue+2, 1, 1)
    SI_DG_pt_.addLatex(0.9, 0.93, 'Displaced Global Muons: |#eta^{DG}| < 2', size = 0.04, align = 31)
    SI_DG_pt_.saveRatio(1, 0, 1, '', SI_matched_DG_pt, BCK_matched_DG_pt, r_ymin=0, r_ymax=500, label ="Sig/Bkg", outputDir = 'harvested_diffs/')


    # Differences in sigma/pt
    BCK_unmatched_DG_pt = getObject('fakes_DY2M_ptmin31/th1fs.root', 'unmatched_DG_ptSig')
    SI_unmatched_DG_pt = getObject('fakes_signal_ptmin31/th1fs.root', 'unmatched_DG_ptSig')
    BCK_unmatched_DG_pt.Scale(1.0/BCK_unmatched_DG_pt.Integral())
    SI_unmatched_DG_pt.Scale(1.0/SI_unmatched_DG_pt.Integral())
    BCK_unmatched_DG_pt.SetLineWidth(2)
    SI_unmatched_DG_pt.SetLineWidth(2)
    BCK_unmatched_DG_pt.SetTitle(';Fake DG #sigma_{p_{T}}/p_{T};Normalized fake DG yield')
    SI_unmatched_DG_pt.SetTitle('')
    SI_DG_pt_ = Canvas.Canvas("unmatched_comp_ptSig", 'png', 0.35, 0.73, 0.67, 0.82, 1) 
    SI_DG_pt_.addHisto(BCK_unmatched_DG_pt, 'HIST', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'l', r.kRed+2, 1, 0)
    SI_DG_pt_.addHisto(SI_unmatched_DG_pt, 'HIST,SAME', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'l', r.kBlue+2, 1, 1)
    SI_DG_pt_.addLatex(0.87, 0.86, 'Displaced Global Muons: |#eta^{DG}| < 2, p_{T}^{DG} > 31 GeV', size = 0.036, align = 31)
    SI_DG_pt_.saveRatio(1, 0, 1, '', SI_unmatched_DG_pt, BCK_unmatched_DG_pt, r_ymin=0, r_ymax=2, label ="Sig/Bkg", outputDir = 'harvested_diffs/')


    BCK_matched_DG_pt = getObject('fakes_DY2M_ptmin31/th1fs.root', 'matched_DG_ptSig')
    SI_matched_DG_pt = getObject('fakes_signal_ptmin31/th1fs.root', 'matched_DG_ptSig')
    BCK_matched_DG_pt.Scale(1.0/BCK_matched_DG_pt.Integral())
    SI_matched_DG_pt.Scale(1.0/SI_matched_DG_pt.Integral())
    BCK_matched_DG_pt.SetLineWidth(2)
    SI_matched_DG_pt.SetLineWidth(2)
    BCK_matched_DG_pt.SetTitle(';True DG #sigma_{p_{T}}/p_{T};Normalized true DG yield')
    SI_matched_DG_pt.SetTitle('')
    SI_DG_pt_ = Canvas.Canvas("matched_comp_ptSig", 'png', 0.35, 0.73, 0.67, 0.82, 1) 
    SI_DG_pt_.addHisto(BCK_matched_DG_pt, 'HIST', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'l', r.kRed+2, 1, 0)
    SI_DG_pt_.addHisto(SI_matched_DG_pt, 'HIST,SAME', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'l', r.kBlue+2, 1, 1)
    SI_DG_pt_.addLatex(0.87, 0.86, 'Displaced Global Muons: |#eta^{DG}| < 2, p_{T}^{DG} > 31 GeV', size = 0.036, align = 31)
    SI_DG_pt_.saveRatio(1, 0, 1, '', SI_matched_DG_pt, BCK_matched_DG_pt, r_ymin=0, r_ymax=20, label ="Sig/Bkg", outputDir = 'harvested_diffs/')



