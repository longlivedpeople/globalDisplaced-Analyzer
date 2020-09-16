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

    # ptmin > 31, eta cut 
    SI_DG_sigmapt = getObject('resolutions_signal_ptmin31_sigma0p2sep/th1fs.root', 'hist_DG_sigmapt') 
    SI_DG_sigmapt.SetTitle(';DG #sigma_{p_{T}}/p_{T};DG yield')
    SI_DG_sigmapt.SetLineWidth(1)
    SI_DG_sigmapt.SetLineColor(r.kBlack)
    SI_DG_sigmapt.SetFillColorAlpha(r.kBlack, 0.25)
    SI_DG_sigmapt_ = Canvas.Canvas("SI_DG_sigmapt", 'png', 0.57, 0.75, 0.87, 0.9, 1)
    SI_DG_sigmapt_.addHisto(SI_DG_sigmapt, 'HIST', '', 'l', '', 1, 0)
    SI_DG_sigmapt_.addLatex(0.85, 0.85, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31)
    SI_DG_sigmapt_.addLatex(0.85, 0.8, '|#eta^{DG} < 2.4|, p_{T}^{DG} > 10 GeV', size = 0.03, align = 31)
    SI_DG_sigmapt_.save(0, 0, 1, '','', ymin = 0.1, ymax = 5000000, outputDir = WORKPATH + 'harvested_resols_'+opts.tag+'/')

    SI_DG_sigmapt_pass = getObject('resolutions_signal_ptmin31_sigma0p3sep/th1fs.root', 'ptres_DG_sigmapt_bin1') 
    SI_DG_sigmapt_nopass = getObject('resolutions_signal_ptmin31_sigma0p3sep/th1fs.root', 'ptres_DG_sigmapt_bin2') 
    SI_DG_sigmapt_pass.SetTitle(';(p_{T}^{reco}-p_{T}^{gen})/p^{gen}_{T};DG yield')
    SI_DG_sigmapt_nopass.SetTitle(';;')
    SI_DG_sigmapt_pass.SetLineWidth(2)
    SI_DG_sigmapt_nopass.SetLineWidth(2)
    SI_DG_sigmapt_pass.SetLineColor(r.kGreen+2)
    SI_DG_sigmapt_nopass.SetLineColor(r.kRed)
    SI_DG_sigmapt_pass.Scale(1.0/SI_DG_sigmapt_pass.Integral())
    SI_DG_sigmapt_nopass.Scale(1.0/SI_DG_sigmapt_nopass.Integral())
    SI_DG_sigmapt_pass.SetMaximum(0.4)
    SI_DG_sigmapt_cut = Canvas.Canvas("SI_DG_sigmapt_cut", 'png', 0.57, 0.67, 0.87, 0.76, 1)
    SI_DG_sigmapt_cut.addHisto(SI_DG_sigmapt_pass, 'HIST', '#sigma_{p_{T}}/p_{T} < 0.3', 'l', '', 1, 0)
    SI_DG_sigmapt_cut.addHisto(SI_DG_sigmapt_nopass, 'HIST,SAME', '#sigma_{p_{T}}/p_{T} > 0.3', 'l', '', 1, 0)
    SI_DG_sigmapt_cut.addLatex(0.85, 0.85, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_DG_sigmapt_cut.addLatex(0.85, 0.8, '|#eta^{DG}| < 2|, p_{T}^{DG} > 31 GeV', size = 0.03, align = 31)
    SI_DG_sigmapt_cut.addLatex(0.9, 0.93, 'Distributions normalized to 1', font = 62, size = 0.033, align = 31)
    SI_DG_sigmapt_cut.save(1, 0, 0, '','', ymin = 0, outputDir = WORKPATH + 'harvested_resols_'+opts.tag+'/')

    SI_ptres_DG_sigmapt_bin2_0p2 = getObject('resolutions_signal_ptmin31_sigma0p2sep/th1fs.root', 'ptres_DG_sigmapt_bin2')
    SI_ptres_DG_sigmapt_bin2_0p3 = getObject('resolutions_signal_ptmin31_sigma0p3sep/th1fs.root', 'ptres_DG_sigmapt_bin2')
    SI_ptres_DG_sigmapt_bin2_0p4 = getObject('resolutions_signal_ptmin31_sigma0p4sep/th1fs.root', 'ptres_DG_sigmapt_bin2')
    SI_ptres_DG_sigmapt_bin2_0p5 = getObject('resolutions_signal_ptmin31_sigma0p5sep/th1fs.root', 'ptres_DG_sigmapt_bin2')
    SI_ptres_DG_sigmapt_bin2_0p2.SetTitle(';(p_{T}^{DG}-p_{T}^{gen})/p_{T}^{gen};DG yield')
    SI_ptres_DG_sigmapt_bin2_0p3.SetTitle(';;')
    SI_ptres_DG_sigmapt_bin2_0p4.SetTitle(';;')
    SI_ptres_DG_sigmapt_bin2_0p5.SetTitle(';;')
    SI_ptres_DG_sigmapt_bin2_0p2.Rebin(3)
    SI_ptres_DG_sigmapt_bin2_0p3.Rebin(3)
    SI_ptres_DG_sigmapt_bin2_0p4.Rebin(3)
    SI_ptres_DG_sigmapt_bin2_0p5.Rebin(3)
    SI_ptres_DG_sigmapt_bin2_0p2.SetLineWidth(2)
    SI_ptres_DG_sigmapt_bin2_0p3.SetLineWidth(2)
    SI_ptres_DG_sigmapt_bin2_0p4.SetLineWidth(2)
    SI_ptres_DG_sigmapt_bin2_0p5.SetLineWidth(2)

    SI_ptres_DG_sigmapt_bin2_0p2.SetMaximum(SI_ptres_DG_sigmapt_bin2_0p2.GetMaximum()*1.6)
    SI_DG_sigmapt_bin2 = Canvas.Canvas("SI_ptres_DG_sigmapt_bin2", 'png', 0.54, 0.6, 0.85, 0.75, 1) 
    SI_DG_sigmapt_bin2.addHisto(SI_ptres_DG_sigmapt_bin2_0p2, 'HIST', '#sigma_{p_{T}}/p_{T} > 0.2 (0.34%)', 'l', r.kBlack, 1, 0)
    SI_DG_sigmapt_bin2.addHisto(SI_ptres_DG_sigmapt_bin2_0p3, 'HIST,SAME', '#sigma_{p_{T}}/p_{T} > 0.3 (0.19%)', 'l', r.kRed+2, 1, 1)
    SI_DG_sigmapt_bin2.addHisto(SI_ptres_DG_sigmapt_bin2_0p4, 'HIST,SAME', '#sigma_{p_{T}}/p_{T} > 0.4 (0.14%)', 'l', r.kRed-4, 1, 2)
    SI_DG_sigmapt_bin2.addHisto(SI_ptres_DG_sigmapt_bin2_0p5, 'HIST,SAME', '#sigma_{p_{T}}/p_{T} > 0.5 (0.11%)', 'l', r.kRed-7, 1, 3)
    SI_DG_sigmapt_bin2.addLatex(0.85, 0.85, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31)
    SI_DG_sigmapt_bin2.addLatex(0.85, 0.8, '|#eta^{DG}| < 2|, p_{T}^{DG} > 31 GeV', size = 0.03, align = 31)
    SI_DG_sigmapt_bin2.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_resols_'+opts.tag+'/', maxYnumbers = 3)


