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

    SI_matched_DG_normChi2 = getObject('fakes_signal_ptmin10_sigmapt0p4/th1fs.root', 'matched_DG_normChi2')
    SI_unmatched_DG_normChi2 = getObject('fakes_signal_ptmin10_sigmapt0p4/th1fs.root', 'unmatched_DG_normChi2')
    SI_DG_normChi2 = doFakeStack(SI_matched_DG_normChi2, SI_unmatched_DG_normChi2)
    SI_DG_normChi2.SetMinimum(10)
    SI_DG_normChi2.SetMaximum(1e7)
    SI_DG_normChi2_ = Canvas.Canvas("SI_DG_normChi2", 'png', 0.52, 0.81, 0.87, 0.9, 1)
    SI_DG_normChi2_.addStack(SI_DG_normChi2, 'HIST', 1, 0)
    SI_DG_normChi2_.addLatex(0.35, 0.75, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 11)
    SI_DG_normChi2_.addLatex(0.35, 0.70, 'p_{T}^{DG} > 10 GeV, |#eta^{DG}| < 2.4', size = 0.03, align = 11)
    SI_DG_normChi2_.addLatex(0.35, 0.65, '#sigma_{p_{T}}/p_{T} < 0.4', size = 0.03, align = 11)
    SI_DG_normChi2_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_normChi2cut_'+opts.tag+'/')


    DY_matched_DG_normChi2 = getObject('fakes_DY2M_ptmin10_sigmapt0p4/th1fs.root', 'matched_DG_normChi2')
    DY_unmatched_DG_normChi2 = getObject('fakes_DY2M_ptmin10_sigmapt0p4/th1fs.root', 'unmatched_DG_normChi2')
    DY_DG_normChi2 = doFakeStack(DY_matched_DG_normChi2, DY_unmatched_DG_normChi2)
    DY_DG_normChi2.SetMinimum(10)
    DY_DG_normChi2.SetMaximum(1e7)
    DY_DG_normChi2_ = Canvas.Canvas("DY_DG_normChi2", 'png', 0.52, 0.81, 0.87, 0.9, 1)
    DY_DG_normChi2_.addStack(DY_DG_normChi2, 'HIST', 1, 0)
    DY_DG_normChi2_.addLatex(0.35, 0.75, 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', font = 62,size = 0.03, align = 11)
    DY_DG_normChi2_.addLatex(0.35, 0.70, 'p_{T}^{DG} > 10 GeV, |#eta^{DG}| < 2.4', size = 0.03, align = 11)
    DY_DG_normChi2_.addLatex(0.35, 0.65, '#sigma_{p_{T}}/p_{T} < 0.4', size = 0.03, align = 11)
    DY_DG_normChi2_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_normChi2cut_'+opts.tag+'/')


    SI_DG_normChi2 = getObject('fakes_signal_ptmin10_sigmapt0p4/th1fs.root', 'pfake_DG_normChi2')
    DY_DG_normChi2 = getObject('fakes_DY2M_ptmin10_sigmapt0p4/th1fs.root', 'pfake_DG_normChi2')
    DY_DG_normChi2.SetTitle(';DG #chi^{2}/ndof;Fake rate')
    SI_DG_normChi2.SetTitle(';;')
    SI_DG_normChi2_ = Canvas.Canvas("fake_DG_normChi2_log", 'png', 0.31, 0.78, 0.53, 0.9, 1)
    SI_DG_normChi2_.addRate(DY_DG_normChi2, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed+2, 1, 0, marker = 24)
    SI_DG_normChi2_.addRate(SI_DG_normChi2, 'AP,SAME', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'p', r.kBlue+2, 1, 1, marker = 24)
    #SI_DG_normChi2_.addLatex(0.85, 0.85, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31)
    SI_DG_normChi2_.addLatex(0.41, 0.75, 'p_{T}^{DG} > 10 GeV, |#eta^{DG}| < 2.4', size = 0.03, align = 11)
    SI_DG_normChi2_.addLatex(0.41, 0.7, '#sigma_{p_{T}}/p_{T} < 0.4', size = 0.03, align = 11)
    SI_DG_normChi2_.save(1, 0, 0, '','', xlog = True, outputDir = WORKPATH + 'harvested_fakes_normChi2cut_'+opts.tag+'/')

