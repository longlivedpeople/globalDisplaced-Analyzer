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



    ###################################
    ####   Construct Resolutions   ####
    ###################################

    # ptmin > 10, eta cut 
    SI_DG_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt') 
    SI_DGID_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt') 
    SI_GM_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt') 
    SI_DG_pt.Scale(1.0/SI_DG_pt.Integral())
    SI_GM_pt.Scale(1.0/SI_GM_pt.Integral())
    SI_DGID_pt.Scale(1.0/SI_DGID_pt.Integral())
    SI_DG_pt.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p^{gen}_{T};Normalized muon yield')
    SI_DG_pt.SetLineWidth(2)
    SI_DG_pt.SetLineColor(r.kBlack)
    SI_DGID_pt.SetTitle(';;')
    SI_DGID_pt.SetLineWidth(2)
    SI_DGID_pt.SetLineColor(r.kBlue+1)
    SI_GM_pt.SetTitle(';;')
    SI_GM_pt.SetLineWidth(2)
    SI_GM_pt.SetLineColor(r.kRed-7)
    SI_DG_pt.SetMaximum(0.17)
    SI_allMU_pt_ = Canvas.Canvas("SI_allMU_pt", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_pt_.addHisto(SI_DG_pt, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_pt_.addHisto(SI_DGID_pt, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_pt_.addHisto(SI_GM_pt, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_pt_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')

    #####################################

    SI_DG_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_dxy') 
    SI_DGID_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_dxy') 
    SI_GM_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_dxy') 
    SI_DG_dxy.Scale(1.0/SI_DG_dxy.Integral())
    SI_GM_dxy.Scale(1.0/SI_GM_dxy.Integral())
    SI_DGID_dxy.Scale(1.0/SI_DGID_dxy.Integral())
    SI_DG_dxy.SetTitle(';(d_{xy}^{reco} - d_{xy}^{gen})/d^{gen}_{xy};Normalized muon yield')
    SI_DG_dxy.SetLineWidth(2)
    SI_DG_dxy.SetLineColor(r.kBlack)
    SI_DGID_dxy.SetTitle(';;')
    SI_DGID_dxy.SetLineWidth(2)
    SI_DGID_dxy.SetLineColor(r.kBlue+1)
    SI_GM_dxy.SetTitle(';;')
    SI_GM_dxy.SetLineWidth(2)
    SI_GM_dxy.SetLineColor(r.kRed-7)
    SI_DG_dxy.SetMaximum(0.35)
    SI_allMU_dxy_ = Canvas.Canvas("SI_allMU_dxy", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_dxy_.addHisto(SI_DG_dxy, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_dxy_.addHisto(SI_DGID_dxy, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_dxy_.addHisto(SI_GM_dxy, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_dxy_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################
    # Lxy bins pt
    #####################################

    SI_DG_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_Lxybin1') 
    SI_DGID_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_Lxybin1') 
    SI_GM_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_Lxybin1') 
    SI_DG_pt.Scale(1.0/SI_DG_pt.Integral())
    SI_GM_pt.Scale(1.0/SI_GM_pt.Integral())
    SI_DGID_pt.Scale(1.0/SI_DGID_pt.Integral())
    SI_DG_pt.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p^{gen}_{T};Normalized muon yield')
    SI_DG_pt.SetLineWidth(2)
    SI_DG_pt.SetLineColor(r.kBlack)
    SI_DGID_pt.SetTitle(';;')
    SI_DGID_pt.SetLineWidth(2)
    SI_DGID_pt.SetLineColor(r.kBlue+1)
    SI_GM_pt.SetTitle(';;')
    SI_GM_pt.SetLineWidth(2)
    SI_GM_pt.SetLineColor(r.kRed-7)
    SI_DG_pt.SetMaximum(0.17)
    SI_allMU_pt_ = Canvas.Canvas("SI_allMU_pt_Lxybin1", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_pt_.addHisto(SI_DG_pt, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_pt_.addHisto(SI_DGID_pt, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_pt_.addHisto(SI_GM_pt, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_pt_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')

    #####################################

    SI_DG_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_Lxybin2') 
    SI_DGID_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_Lxybin2') 
    SI_GM_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_Lxybin2') 
    SI_DG_pt.Scale(1.0/SI_DG_pt.Integral())
    SI_GM_pt.Scale(1.0/SI_GM_pt.Integral())
    SI_DGID_pt.Scale(1.0/SI_DGID_pt.Integral())
    SI_DG_pt.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p^{gen}_{T};Normalized muon yield')
    SI_DG_pt.SetLineWidth(2)
    SI_DG_pt.SetLineColor(r.kBlack)
    SI_DGID_pt.SetTitle(';;')
    SI_DGID_pt.SetLineWidth(2)
    SI_DGID_pt.SetLineColor(r.kBlue+1)
    SI_GM_pt.SetTitle(';;')
    SI_GM_pt.SetLineWidth(2)
    SI_GM_pt.SetLineColor(r.kRed-7)
    SI_DG_pt.SetMaximum(0.17)
    SI_allMU_pt_ = Canvas.Canvas("SI_allMU_pt_Lxybin2", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_pt_.addHisto(SI_DG_pt, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_pt_.addHisto(SI_DGID_pt, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_pt_.addHisto(SI_GM_pt, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_pt_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')



    #####################################

    SI_DG_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_Lxybin3') 
    SI_DGID_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_Lxybin3') 
    SI_GM_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_Lxybin3') 
    SI_DG_pt.Scale(1.0/SI_DG_pt.Integral())
    SI_GM_pt.Scale(1.0/SI_GM_pt.Integral())
    SI_DGID_pt.Scale(1.0/SI_DGID_pt.Integral())
    SI_DG_pt.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p^{gen}_{T};Normalized muon yield')
    SI_DG_pt.SetLineWidth(2)
    SI_DG_pt.SetLineColor(r.kBlack)
    SI_DGID_pt.SetTitle(';;')
    SI_DGID_pt.SetLineWidth(2)
    SI_DGID_pt.SetLineColor(r.kBlue+1)
    SI_GM_pt.SetTitle(';;')
    SI_GM_pt.SetLineWidth(2)
    SI_GM_pt.SetLineColor(r.kRed-7)
    SI_DG_pt.SetMaximum(0.17)
    SI_allMU_pt_ = Canvas.Canvas("SI_allMU_pt_Lxybin3", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_pt_.addHisto(SI_DG_pt, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_pt_.addHisto(SI_DGID_pt, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_pt_.addHisto(SI_GM_pt, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_pt_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################

    SI_DG_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_Lxybin4') 
    SI_DGID_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_Lxybin4') 
    SI_GM_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_Lxybin4') 
    SI_DG_pt.Scale(1.0/SI_DG_pt.Integral())
    SI_GM_pt.Scale(1.0/SI_GM_pt.Integral())
    SI_DGID_pt.Scale(1.0/SI_DGID_pt.Integral())
    SI_DG_pt.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p^{gen}_{T};Normalized muon yield')
    SI_DG_pt.SetLineWidth(2)
    SI_DG_pt.SetLineColor(r.kBlack)
    SI_DGID_pt.SetTitle(';;')
    SI_DGID_pt.SetLineWidth(2)
    SI_DGID_pt.SetLineColor(r.kBlue+1)
    SI_GM_pt.SetTitle(';;')
    SI_GM_pt.SetLineWidth(2)
    SI_GM_pt.SetLineColor(r.kRed-7)
    SI_DG_pt.SetMaximum(0.17)
    SI_allMU_pt_ = Canvas.Canvas("SI_allMU_pt_Lxybin4", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_pt_.addHisto(SI_DG_pt, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_pt_.addHisto(SI_DGID_pt, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    #SI_allMU_pt_.addHisto(SI_GM_pt, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_pt_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################


    #####################################
    # dxy bins pt
    #####################################

    SI_DG_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_dxybin1') 
    SI_DGID_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_dxybin1') 
    SI_GM_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_dxybin1') 
    SI_DG_pt.Scale(1.0/SI_DG_pt.Integral())
    SI_GM_pt.Scale(1.0/SI_GM_pt.Integral())
    SI_DGID_pt.Scale(1.0/SI_DGID_pt.Integral())
    SI_DG_pt.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p^{gen}_{T};Normalized muon yield')
    SI_DG_pt.SetLineWidth(2)
    SI_DG_pt.SetLineColor(r.kBlack)
    SI_DGID_pt.SetTitle(';;')
    SI_DGID_pt.SetLineWidth(2)
    SI_DGID_pt.SetLineColor(r.kBlue+1)
    SI_GM_pt.SetTitle(';;')
    SI_GM_pt.SetLineWidth(2)
    SI_GM_pt.SetLineColor(r.kRed-7)
    SI_DG_pt.SetMaximum(0.17)
    SI_allMU_pt_ = Canvas.Canvas("SI_allMU_pt_dxybin1", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_pt_.addHisto(SI_DG_pt, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_pt_.addHisto(SI_DGID_pt, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_pt_.addHisto(SI_GM_pt, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_pt_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')

    #####################################

    SI_DG_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_dxybin2') 
    SI_DGID_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_dxybin2') 
    SI_GM_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_dxybin2') 
    SI_DG_pt.Scale(1.0/SI_DG_pt.Integral())
    SI_GM_pt.Scale(1.0/SI_GM_pt.Integral())
    SI_DGID_pt.Scale(1.0/SI_DGID_pt.Integral())
    SI_DG_pt.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p^{gen}_{T};Normalized muon yield')
    SI_DG_pt.SetLineWidth(2)
    SI_DG_pt.SetLineColor(r.kBlack)
    SI_DGID_pt.SetTitle(';;')
    SI_DGID_pt.SetLineWidth(2)
    SI_DGID_pt.SetLineColor(r.kBlue+1)
    SI_GM_pt.SetTitle(';;')
    SI_GM_pt.SetLineWidth(2)
    SI_GM_pt.SetLineColor(r.kRed-7)
    SI_DG_pt.SetMaximum(0.17)
    SI_allMU_pt_ = Canvas.Canvas("SI_allMU_pt_dxybin2", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_pt_.addHisto(SI_DG_pt, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_pt_.addHisto(SI_DGID_pt, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_pt_.addHisto(SI_GM_pt, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_pt_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')



    #####################################

    SI_DG_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_dxybin3') 
    SI_DGID_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_dxybin3') 
    SI_GM_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_dxybin3') 
    SI_DG_pt.Scale(1.0/SI_DG_pt.Integral())
    SI_GM_pt.Scale(1.0/SI_GM_pt.Integral())
    SI_DGID_pt.Scale(1.0/SI_DGID_pt.Integral())
    SI_DG_pt.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p^{gen}_{T};Normalized muon yield')
    SI_DG_pt.SetLineWidth(2)
    SI_DG_pt.SetLineColor(r.kBlack)
    SI_DGID_pt.SetTitle(';;')
    SI_DGID_pt.SetLineWidth(2)
    SI_DGID_pt.SetLineColor(r.kBlue+1)
    SI_GM_pt.SetTitle(';;')
    SI_GM_pt.SetLineWidth(2)
    SI_GM_pt.SetLineColor(r.kRed-7)
    SI_DG_pt.SetMaximum(0.17)
    SI_allMU_pt_ = Canvas.Canvas("SI_allMU_pt_dxybin3", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_pt_.addHisto(SI_DG_pt, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_pt_.addHisto(SI_DGID_pt, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_pt_.addHisto(SI_GM_pt, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_pt_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################

    SI_DG_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_dxybin4') 
    SI_DGID_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_dxybin4') 
    SI_GM_pt = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_dxybin4') 
    SI_DG_pt.Scale(1.0/SI_DG_pt.Integral())
    SI_GM_pt.Scale(1.0/SI_GM_pt.Integral())
    SI_DGID_pt.Scale(1.0/SI_DGID_pt.Integral())
    SI_DG_pt.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p^{gen}_{T};Normalized muon yield')
    SI_DG_pt.SetLineWidth(2)
    SI_DG_pt.SetLineColor(r.kBlack)
    SI_DGID_pt.SetTitle(';;')
    SI_DGID_pt.SetLineWidth(2)
    SI_DGID_pt.SetLineColor(r.kBlue+1)
    SI_GM_pt.SetTitle(';;')
    SI_GM_pt.SetLineWidth(2)
    SI_GM_pt.SetLineColor(r.kRed-7)
    SI_DG_pt.SetMaximum(0.17)
    SI_allMU_pt_ = Canvas.Canvas("SI_allMU_pt_dxybin4", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_pt_.addHisto(SI_DG_pt, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_pt_.addHisto(SI_DGID_pt, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    #SI_allMU_pt_.addHisto(SI_GM_pt, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_pt_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################


    #####################################
    # Lxy bins pt
    #####################################

    SI_DG_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_dxy_Lxybin1') 
    SI_DGID_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_dxy_Lxybin1') 
    SI_GM_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_dxy_Lxybin1') 
    SI_DG_dxy.Scale(1.0/SI_DG_dxy.Integral())
    SI_GM_dxy.Scale(1.0/SI_GM_dxy.Integral())
    SI_DGID_dxy.Scale(1.0/SI_DGID_dxy.Integral())
    SI_DG_dxy.SetTitle(';(d_{xy}^{reco} - d_{xy}^{gen})/d^{gen}_{xy};Normalized muon yield')
    SI_DG_dxy.SetLineWidth(2)
    SI_DG_dxy.SetLineColor(r.kBlack)
    SI_DGID_dxy.SetTitle(';;')
    SI_DGID_dxy.SetLineWidth(2)
    SI_DGID_dxy.SetLineColor(r.kBlue+1)
    SI_GM_dxy.SetTitle(';;')
    SI_GM_dxy.SetLineWidth(2)
    SI_GM_dxy.SetLineColor(r.kRed-7)
    SI_DG_dxy.SetMaximum(0.3)
    SI_allMU_dxy_ = Canvas.Canvas("SI_allMU_dxy_Lxybin1", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_dxy_.addHisto(SI_DG_dxy, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_dxy_.addHisto(SI_DGID_dxy, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_dxy_.addHisto(SI_GM_dxy, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_dxy_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')

    #####################################

    SI_DG_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_dxy_Lxybin2') 
    SI_DGID_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_dxy_Lxybin2') 
    SI_GM_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_dxy_Lxybin2') 
    SI_DG_dxy.Scale(1.0/SI_DG_dxy.Integral())
    SI_GM_dxy.Scale(1.0/SI_GM_dxy.Integral())
    SI_DGID_dxy.Scale(1.0/SI_DGID_dxy.Integral())
    SI_DG_dxy.SetTitle(';(d_{xy}^{reco} - d_{xy}^{gen})/d^{gen}_{xy};Normalized muon yield')
    SI_DG_dxy.SetLineWidth(2)
    SI_DG_dxy.SetLineColor(r.kBlack)
    SI_DGID_dxy.SetTitle(';;')
    SI_DGID_dxy.SetLineWidth(2)
    SI_DGID_dxy.SetLineColor(r.kBlue+1)
    SI_GM_dxy.SetTitle(';;')
    SI_GM_dxy.SetLineWidth(2)
    SI_GM_dxy.SetLineColor(r.kRed-7)
    SI_DG_dxy.SetMaximum(0.5)
    SI_allMU_dxy_ = Canvas.Canvas("SI_allMU_dxy_Lxybin2", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_dxy_.addHisto(SI_DG_dxy, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_dxy_.addHisto(SI_DGID_dxy, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_dxy_.addHisto(SI_GM_dxy, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_dxy_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')



    #####################################

    SI_DG_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_dxy_Lxybin3') 
    SI_DGID_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_dxy_Lxybin3') 
    SI_GM_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_dxy_Lxybin3') 
    SI_DG_dxy.Scale(1.0/SI_DG_dxy.Integral())
    SI_GM_dxy.Scale(1.0/SI_GM_dxy.Integral())
    SI_DGID_dxy.Scale(1.0/SI_DGID_dxy.Integral())
    SI_DG_dxy.SetTitle(';(d_{xy}^{reco} - d_{xy}^{gen})/d^{gen}_{xy};Normalized muon yield')
    SI_DG_dxy.SetLineWidth(2)
    SI_DG_dxy.SetLineColor(r.kBlack)
    SI_DGID_dxy.SetTitle(';;')
    SI_DGID_dxy.SetLineWidth(2)
    SI_DGID_dxy.SetLineColor(r.kBlue+1)
    SI_GM_dxy.SetTitle(';;')
    SI_GM_dxy.SetLineWidth(2)
    SI_GM_dxy.SetLineColor(r.kRed-7)
    SI_DG_dxy.SetMaximum(0.3)
    SI_allMU_dxy_ = Canvas.Canvas("SI_allMU_dxy_Lxybin3", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_dxy_.addHisto(SI_DG_dxy, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_dxy_.addHisto(SI_DGID_dxy, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_dxy_.addHisto(SI_GM_dxy, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_dxy_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################

    SI_DG_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_dxy_Lxybin4') 
    SI_DGID_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_dxy_Lxybin4') 
    SI_GM_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_dxy_Lxybin4') 
    SI_DG_dxy.Scale(1.0/SI_DG_dxy.Integral())
    SI_GM_dxy.Scale(1.0/SI_GM_dxy.Integral())
    SI_DGID_dxy.Scale(1.0/SI_DGID_dxy.Integral())
    SI_DG_dxy.SetTitle(';(d_{xy}^{reco} - d_{xy}^{gen})/d^{gen}_{xy};Normalized muon yield')
    SI_DG_dxy.SetLineWidth(2)
    SI_DG_dxy.SetLineColor(r.kBlack)
    SI_DGID_dxy.SetTitle(';;')
    SI_DGID_dxy.SetLineWidth(2)
    SI_DGID_dxy.SetLineColor(r.kBlue+1)
    SI_GM_dxy.SetTitle(';;')
    SI_GM_dxy.SetLineWidth(2)
    SI_GM_dxy.SetLineColor(r.kRed-7)
    SI_DG_dxy.SetMaximum(0.2)
    SI_allMU_dxy_ = Canvas.Canvas("SI_allMU_dxy_Lxybin4", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_dxy_.addHisto(SI_DG_dxy, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_dxy_.addHisto(SI_DGID_dxy, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    #SI_allMU_dxy_.addHisto(SI_GM_dxy, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_dxy_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################


    #####################################
    # dxy bins pt
    #####################################

    SI_DG_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_dxy_dxybin1') 
    SI_DGID_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_dxy_dxybin1') 
    SI_GM_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_dxy_dxybin1') 
    SI_DG_dxy.Scale(1.0/SI_DG_dxy.Integral())
    SI_GM_dxy.Scale(1.0/SI_GM_dxy.Integral())
    SI_DGID_dxy.Scale(1.0/SI_DGID_dxy.Integral())
    SI_DG_dxy.SetTitle(';(d_{xy}^{reco} - d_{xy}^{gen})/d^{gen}_{xy};Normalized muon yield')
    SI_DG_dxy.SetLineWidth(2)
    SI_DG_dxy.SetLineColor(r.kBlack)
    SI_DGID_dxy.SetTitle(';;')
    SI_DGID_dxy.SetLineWidth(2)
    SI_DGID_dxy.SetLineColor(r.kBlue+1)
    SI_GM_dxy.SetTitle(';;')
    SI_GM_dxy.SetLineWidth(2)
    SI_GM_dxy.SetLineColor(r.kRed-7)
    SI_DG_dxy.SetMaximum(0.3)
    SI_allMU_dxy_ = Canvas.Canvas("SI_allMU_dxy_dxybin1", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_dxy_.addHisto(SI_DG_dxy, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_dxy_.addHisto(SI_DGID_dxy, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_dxy_.addHisto(SI_GM_dxy, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_dxy_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')

    #####################################

    SI_DG_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_dxy_dxybin2') 
    SI_DGID_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_dxy_dxybin2') 
    SI_GM_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_dxy_dxybin2') 
    SI_DG_dxy.Scale(1.0/SI_DG_dxy.Integral())
    SI_GM_dxy.Scale(1.0/SI_GM_dxy.Integral())
    SI_DGID_dxy.Scale(1.0/SI_DGID_dxy.Integral())
    SI_DG_dxy.SetTitle(';(d_{xy}^{reco} - d_{xy}^{gen})/d^{gen}_{xy};Normalized muon yield')
    SI_DG_dxy.SetLineWidth(2)
    SI_DG_dxy.SetLineColor(r.kBlack)
    SI_DGID_dxy.SetTitle(';;')
    SI_DGID_dxy.SetLineWidth(2)
    SI_DGID_dxy.SetLineColor(r.kBlue+1)
    SI_GM_dxy.SetTitle(';;')
    SI_GM_dxy.SetLineWidth(2)
    SI_GM_dxy.SetLineColor(r.kRed-7)
    SI_DG_dxy.SetMaximum(0.5)
    SI_allMU_dxy_ = Canvas.Canvas("SI_allMU_dxy_dxybin2", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_dxy_.addHisto(SI_DG_dxy, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_dxy_.addHisto(SI_DGID_dxy, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_dxy_.addHisto(SI_GM_dxy, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_dxy_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')



    #####################################

    SI_DG_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_dxy_dxybin3') 
    SI_DGID_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_dxy_dxybin3') 
    SI_GM_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_dxy_dxybin3') 
    SI_DG_dxy.Scale(1.0/SI_DG_dxy.Integral())
    SI_GM_dxy.Scale(1.0/SI_GM_dxy.Integral())
    SI_DGID_dxy.Scale(1.0/SI_DGID_dxy.Integral())
    SI_DG_dxy.SetTitle(';(d_{xy}^{reco} - d_{xy}^{gen})/d^{gen}_{xy};Normalized muon yield')
    SI_DG_dxy.SetLineWidth(2)
    SI_DG_dxy.SetLineColor(r.kBlack)
    SI_DGID_dxy.SetTitle(';;')
    SI_DGID_dxy.SetLineWidth(2)
    SI_DGID_dxy.SetLineColor(r.kBlue+1)
    SI_GM_dxy.SetTitle(';;')
    SI_GM_dxy.SetLineWidth(2)
    SI_GM_dxy.SetLineColor(r.kRed-7)
    SI_DG_dxy.SetMaximum(0.5)
    SI_allMU_dxy_ = Canvas.Canvas("SI_allMU_dxy_dxybin3", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_dxy_.addHisto(SI_DG_dxy, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_dxy_.addHisto(SI_DGID_dxy, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    SI_allMU_dxy_.addHisto(SI_GM_dxy, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_dxy_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################

    SI_DG_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_dxy_dxybin4') 
    SI_DGID_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_dxy_dxybin4') 
    #SI_GM_dxy = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_dxy_dxybin4') 
    SI_DG_dxy.Scale(1.0/SI_DG_dxy.Integral())
    #SI_GM_dxy.Scale(1.0/SI_GM_dxy.Integral())
    SI_DGID_dxy.Scale(1.0/SI_DGID_dxy.Integral())
    SI_DG_dxy.SetTitle(';(d_{xy}^{reco} - d_{xy}^{gen})/d^{gen}_{xy};Normalized muon yield')
    SI_DG_dxy.SetLineWidth(2)
    SI_DG_dxy.SetLineColor(r.kBlack)
    SI_DGID_dxy.SetTitle(';;')
    SI_DGID_dxy.SetLineWidth(2)
    SI_DGID_dxy.SetLineColor(r.kBlue+1)
    #SI_GM_dxy.SetTitle(';;')
    #SI_GM_dxy.SetLineWidth(2)
    #SI_GM_dxy.SetLineColor(r.kRed-7)
    #SI_DG_dxy.SetMaximum(0.5)
    SI_allMU_dxy_ = Canvas.Canvas("SI_allMU_dxy_dxybin4", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_dxy_.addHisto(SI_DG_dxy, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_dxy_.addHisto(SI_DGID_dxy, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    #SI_allMU_dxy_.addHisto(SI_GM_dxy, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_dxy_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################

    #
    # Dependence with pT
    #

    #####################################

    ## -> Standard global muons in pt bins

    SI_GM_pt1 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_ptbin1')
    SI_GM_pt2 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_ptbin2')
    SI_GM_pt3 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_ptbin3')
    SI_GM_pt4 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_ptbin4')
    SI_GM_pt1.Scale(1.0/SI_GM_pt1.Integral())
    SI_GM_pt2.Scale(1.0/SI_GM_pt2.Integral())
    SI_GM_pt3.Scale(1.0/SI_GM_pt3.Integral())
    SI_GM_pt4.Scale(1.0/SI_GM_pt4.Integral())
    SI_GM_pt1.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized GM yield')
    SI_GM_pt1.GetYaxis().SetTitleOffset(1.35)
    SI_GM_pt2.SetTitle(';;')
    SI_GM_pt3.SetTitle(';;')
    SI_GM_pt4.SetTitle(';;')
    SI_GM_pt1.SetLineWidth(2)
    SI_GM_pt2.SetLineWidth(2)
    SI_GM_pt3.SetLineWidth(2)
    SI_GM_pt4.SetLineWidth(2)
    SI_GM_pt1.SetMaximum(1.3*SI_GM_pt1.GetMaximum())
    SI_GM_ptbin = Canvas.Canvas("SI_GM_ptbin", 'png', 0.6, 0.58, 0.84, 0.78, 1)
    SI_GM_ptbin.addHisto(SI_GM_pt1, 'HIST', 'p_{T}^{gen} #in (31, 50]', 'l', r.kBlack, 1, 0)
    SI_GM_ptbin.addHisto(SI_GM_pt2, 'HIST, SAME', 'p_{T}^{gen} #in [50, 150]', 'l', r.kBlue+2, 1, 1)
    SI_GM_ptbin.addHisto(SI_GM_pt3, 'HIST, SAME', 'p_{T}^{gen} #in [150, 300]', 'l', r.kBlue-4, 1, 2)
    SI_GM_ptbin.addHisto(SI_GM_pt4, 'HIST, SAME', 'p_{T}^{gen} #in [300, #infty)', 'l', r.kBlue-9, 1, 3)
    SI_GM_ptbin.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_GM_ptbin.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_GM_ptbin.addLatex(0.9, 0.93, 'Standard Global Muons', font = 62, size = 0.03, align = 31)
    SI_GM_ptbin.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    ## -> Displaced global muons in pt bins

    SI_DG_pt1 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_ptbin1')
    SI_DG_pt2 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_ptbin2')
    SI_DG_pt3 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_ptbin3')
    SI_DG_pt4 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_ptbin4')
    SI_DG_pt1.Scale(1.0/SI_DG_pt1.Integral())
    SI_DG_pt2.Scale(1.0/SI_DG_pt2.Integral())
    SI_DG_pt3.Scale(1.0/SI_DG_pt3.Integral())
    SI_DG_pt4.Scale(1.0/SI_DG_pt4.Integral())
    SI_DG_pt1.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized DG yield')
    SI_DG_pt1.GetYaxis().SetTitleOffset(1.35)
    SI_DG_pt2.SetTitle(';;')
    SI_DG_pt3.SetTitle(';;')
    SI_DG_pt4.SetTitle(';;')
    SI_DG_pt1.SetLineWidth(2)
    SI_DG_pt2.SetLineWidth(2)
    SI_DG_pt3.SetLineWidth(2)
    SI_DG_pt4.SetLineWidth(2)
    SI_DG_pt1.SetMaximum(1.3*SI_DG_pt1.GetMaximum())
    SI_DG_ptbin = Canvas.Canvas("SI_DG_ptbin", 'png', 0.6, 0.58, 0.84, 0.78, 1)
    SI_DG_ptbin.addHisto(SI_DG_pt1, 'HIST', 'p_{T}^{gen} #in (31, 50]', 'l', r.kBlack, 1, 0)
    SI_DG_ptbin.addHisto(SI_DG_pt2, 'HIST, SAME', 'p_{T}^{gen} #in [50, 150]', 'l', r.kBlue+2, 1, 1)
    SI_DG_ptbin.addHisto(SI_DG_pt3, 'HIST, SAME', 'p_{T}^{gen} #in [150, 300]', 'l', r.kBlue-4, 1, 2)
    SI_DG_ptbin.addHisto(SI_DG_pt4, 'HIST, SAME', 'p_{T}^{gen} #in [300, #infty)', 'l', r.kBlue-9, 1, 3)
    SI_DG_ptbin.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_DG_ptbin.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_DG_ptbin.addLatex(0.9, 0.93, 'Displaced Global Muons', font = 62, size = 0.03, align = 31)
    SI_DG_ptbin.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    ## -> Displaced global muons (ID applied) in pt bins

    SI_DGID_pt1 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_ptbin1')
    SI_DGID_pt2 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_ptbin2')
    SI_DGID_pt3 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_ptbin3')
    SI_DGID_pt4 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_ptbin4')
    SI_DGID_pt1.Scale(1.0/SI_DGID_pt1.Integral())
    SI_DGID_pt2.Scale(1.0/SI_DGID_pt2.Integral())
    SI_DGID_pt3.Scale(1.0/SI_DGID_pt3.Integral())
    SI_DGID_pt4.Scale(1.0/SI_DGID_pt4.Integral())
    SI_DGID_pt1.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized DGID yield')
    SI_DGID_pt1.GetYaxis().SetTitleOffset(1.35)
    SI_DGID_pt2.SetTitle(';;')
    SI_DGID_pt3.SetTitle(';;')
    SI_DGID_pt4.SetTitle(';;')
    SI_DGID_pt1.SetLineWidth(2)
    SI_DGID_pt2.SetLineWidth(2)
    SI_DGID_pt3.SetLineWidth(2)
    SI_DGID_pt4.SetLineWidth(2)
    SI_DGID_pt1.SetMaximum(1.3*SI_DGID_pt1.GetMaximum())
    SI_DGID_ptbin = Canvas.Canvas("SI_DGID_ptbin", 'png', 0.6, 0.58, 0.84, 0.78, 1)
    SI_DGID_ptbin.addHisto(SI_DGID_pt1, 'HIST', 'p_{T}^{gen} #in (31, 50]', 'l', r.kBlack, 1, 0)
    SI_DGID_ptbin.addHisto(SI_DGID_pt2, 'HIST, SAME', 'p_{T}^{gen} #in [50, 150]', 'l', r.kBlue+2, 1, 1)
    SI_DGID_ptbin.addHisto(SI_DGID_pt3, 'HIST, SAME', 'p_{T}^{gen} #in [150, 300]', 'l', r.kBlue-4, 1, 2)
    SI_DGID_ptbin.addHisto(SI_DGID_pt4, 'HIST, SAME', 'p_{T}^{gen} #in [300, #infty)', 'l', r.kBlue-9, 1, 3)
    SI_DGID_ptbin.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_DGID_ptbin.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} > 31 GeV', size = 0.03, align = 31)
    SI_DGID_ptbin.addLatex(0.9, 0.93, 'Displaced Global Muons (+ ID)', font = 62, size = 0.03, align = 31)
    SI_DGID_ptbin.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    ## -> Pt bin 1: All collections

    SI_GM_pt1 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_ptbin1')
    SI_DG_pt1 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_ptbin1')
    SI_DGID_pt1 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_ptbin1')
    SI_GM_pt1.Scale(1.0/SI_GM_pt1.Integral())
    SI_DG_pt1.Scale(1.0/SI_DG_pt1.Integral())
    SI_DGID_pt1.Scale(1.0/SI_DGID_pt1.Integral())
    SI_DG_pt1.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield')
    SI_DG_pt1.GetYaxis().SetTitleOffset(1.35)
    SI_GM_pt1.SetTitle(';;')
    SI_DGID_pt1.SetTitle(';;')
    SI_GM_pt1.SetLineWidth(2)
    SI_DG_pt1.SetLineWidth(2)
    SI_DGID_pt1.SetLineWidth(2)
    SI_DG_pt1.SetMaximum(1.4*SI_DG_pt1.GetMaximum())
    SI_allMu_ptbin1 = Canvas.Canvas("SI_allMu_ptbin1", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMu_ptbin1.addHisto(SI_DG_pt1, 'HIST', 'Displaced Global', 'l', r.kBlack, 1, 0)
    SI_allMu_ptbin1.addHisto(SI_DGID_pt1, 'HIST, SAME', 'Displaced Global + ID', 'l', r.kBlue+2, 1, 1)
    SI_allMu_ptbin1.addHisto(SI_GM_pt1, 'HIST, SAME', 'Standard Global', 'l', r.kRed-7, 1, 2)
    SI_allMu_ptbin1.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMu_ptbin1.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} #in [31, 50] GeV', size = 0.03, align = 31)
    SI_allMu_ptbin1.addLatex(0.9, 0.94, 'p_{T} bin 1: p_{T} #in [31, 50] GeV', font = 62, size = 0.03, align = 31)
    SI_allMu_ptbin1.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')



    ## -> Pt bin 2: All collections

    SI_GM_pt2 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_ptbin2')
    SI_DG_pt2 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_ptbin2')
    SI_DGID_pt2 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_ptbin2')
    SI_GM_pt2.Scale(1.0/SI_GM_pt2.Integral())
    SI_DG_pt2.Scale(1.0/SI_DG_pt2.Integral())
    SI_DGID_pt2.Scale(1.0/SI_DGID_pt2.Integral())
    SI_DG_pt2.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield')
    SI_DG_pt2.GetYaxis().SetTitleOffset(1.35)
    SI_GM_pt2.SetTitle(';;')
    SI_DGID_pt2.SetTitle(';;')
    SI_GM_pt2.SetLineWidth(2)
    SI_DG_pt2.SetLineWidth(2)
    SI_DGID_pt2.SetLineWidth(2)
    SI_DG_pt2.SetMaximum(1.4*SI_DG_pt2.GetMaximum())
    SI_allMu_ptbin2 = Canvas.Canvas("SI_allMu_ptbin2", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMu_ptbin2.addHisto(SI_DG_pt2, 'HIST', 'Displaced Global', 'l', r.kBlack, 1, 0)
    SI_allMu_ptbin2.addHisto(SI_DGID_pt2, 'HIST, SAME', 'Displaced Global + ID', 'l', r.kBlue+2, 1, 1)
    SI_allMu_ptbin2.addHisto(SI_GM_pt2, 'HIST, SAME', 'Standard Global', 'l', r.kRed-7, 1, 2)
    SI_allMu_ptbin2.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMu_ptbin2.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} #in [50, 150] GeV', size = 0.03, align = 31)
    SI_allMu_ptbin2.addLatex(0.9, 0.94, 'p_{T} bin 2: p_{T} #in [50, 150] GeV', font = 62, size = 0.03, align = 31)
    SI_allMu_ptbin2.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    ## -> Pt bin 3: All collections

    SI_GM_pt3 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_ptbin3')
    SI_DG_pt3 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_ptbin3')
    SI_DGID_pt3 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_ptbin3')
    SI_GM_pt3.Scale(1.0/SI_GM_pt3.Integral())
    SI_DG_pt3.Scale(1.0/SI_DG_pt3.Integral())
    SI_DGID_pt3.Scale(1.0/SI_DGID_pt3.Integral())
    SI_DG_pt3.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield')
    SI_DG_pt3.GetYaxis().SetTitleOffset(1.35)
    SI_GM_pt3.SetTitle(';;')
    SI_DGID_pt3.SetTitle(';;')
    SI_GM_pt3.SetLineWidth(2)
    SI_DG_pt3.SetLineWidth(2)
    SI_DGID_pt3.SetLineWidth(2)
    SI_DG_pt3.SetMaximum(1.4*SI_DG_pt3.GetMaximum())
    SI_allMu_ptbin3 = Canvas.Canvas("SI_allMu_ptbin3", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMu_ptbin3.addHisto(SI_DG_pt3, 'HIST', 'Displaced Global', 'l', r.kBlack, 1, 0)
    SI_allMu_ptbin3.addHisto(SI_DGID_pt3, 'HIST, SAME', 'Displaced Global + ID', 'l', r.kBlue+2, 1, 1)
    SI_allMu_ptbin3.addHisto(SI_GM_pt3, 'HIST, SAME', 'Standard Global', 'l', r.kRed-7, 1, 2)
    SI_allMu_ptbin3.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMu_ptbin3.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} #in [150, 300] GeV', size = 0.03, align = 31)
    SI_allMu_ptbin3.addLatex(0.9, 0.94, 'p_{T} bin 3: p_{T} #in [150, 300] GeV', font = 62, size = 0.03, align = 31)
    SI_allMu_ptbin3.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    ## -> Pt bin 4: All collections

    SI_GM_pt4 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_GM_pt_ptbin4')
    SI_DG_pt4 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DG_pt_ptbin4')
    SI_DGID_pt4 = getObject('plots_signal_ptmin31_eta2/th1fs.root', 'res_DGID_pt_ptbin4')
    SI_GM_pt4.Scale(1.0/SI_GM_pt4.Integral())
    SI_DG_pt4.Scale(1.0/SI_DG_pt4.Integral())
    SI_DGID_pt4.Scale(1.0/SI_DGID_pt4.Integral())
    SI_DG_pt4.SetTitle(';(p_{T}^{reco} - p_{T}^{gen})/p_{T}^{gen};Normalized muon yield')
    SI_DG_pt4.GetYaxis().SetTitleOffset(1.35)
    SI_GM_pt4.SetTitle(';;')
    SI_DGID_pt4.SetTitle(';;')
    SI_GM_pt4.SetLineWidth(2)
    SI_DG_pt4.SetLineWidth(2)
    SI_DGID_pt4.SetLineWidth(2)
    SI_DG_pt4.SetMaximum(1.4*SI_DG_pt4.GetMaximum())
    SI_allMu_ptbin4 = Canvas.Canvas("SI_allMu_ptbin4", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMu_ptbin4.addHisto(SI_DG_pt4, 'HIST', 'Displaced Global', 'l', r.kBlack, 1, 0)
    SI_allMu_ptbin4.addHisto(SI_DGID_pt4, 'HIST, SAME', 'Displaced Global + ID', 'l', r.kBlue+2, 1, 1)
    SI_allMu_ptbin4.addHisto(SI_GM_pt4, 'HIST, SAME', 'Standard Global', 'l', r.kRed-7, 1, 2)
    SI_allMu_ptbin4.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMu_ptbin4.addLatex(0.85, 0.82, '|#eta^{gen}| < 2, p_{T}^{gen} #in [300, #infty) GeV', size = 0.03, align = 31)
    SI_allMu_ptbin4.addLatex(0.9, 0.94, 'p_{T} bin 4: p_{T} #in [300, #infty) GeV', font = 62, size = 0.03, align = 31)
    SI_allMu_ptbin4.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')





