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
    SI_DG_pt = getObject('plots_signal/th1fs.root', 'res_DG_pt') 
    SI_DGID_pt = getObject('plots_signal/th1fs.root', 'res_DGID_pt') 
    SI_GM_pt = getObject('plots_signal/th1fs.root', 'res_GM_pt') 
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
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, p_{T}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')

    #####################################

    SI_DG_dxy = getObject('plots_signal/th1fs.root', 'res_DG_dxy') 
    SI_DGID_dxy = getObject('plots_signal/th1fs.root', 'res_DGID_dxy') 
    SI_GM_dxy = getObject('plots_signal/th1fs.root', 'res_GM_dxy') 
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
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, p_{T}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################
    # Lxy bins pt
    #####################################

    SI_DG_pt = getObject('plots_signal/th1fs.root', 'res_DG_pt_Lxybin1') 
    SI_DGID_pt = getObject('plots_signal/th1fs.root', 'res_DGID_pt_Lxybin1') 
    SI_GM_pt = getObject('plots_signal/th1fs.root', 'res_GM_pt_Lxybin1') 
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
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, p_{T}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')

    #####################################

    SI_DG_pt = getObject('plots_signal/th1fs.root', 'res_DG_pt_Lxybin2') 
    SI_DGID_pt = getObject('plots_signal/th1fs.root', 'res_DGID_pt_Lxybin2') 
    SI_GM_pt = getObject('plots_signal/th1fs.root', 'res_GM_pt_Lxybin2') 
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
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, p_{T}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')



    #####################################

    SI_DG_pt = getObject('plots_signal/th1fs.root', 'res_DG_pt_Lxybin3') 
    SI_DGID_pt = getObject('plots_signal/th1fs.root', 'res_DGID_pt_Lxybin3') 
    SI_GM_pt = getObject('plots_signal/th1fs.root', 'res_GM_pt_Lxybin3') 
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
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, p_{T}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################

    SI_DG_pt = getObject('plots_signal/th1fs.root', 'res_DG_pt_Lxybin4') 
    SI_DGID_pt = getObject('plots_signal/th1fs.root', 'res_DGID_pt_Lxybin4') 
    SI_GM_pt = getObject('plots_signal/th1fs.root', 'res_GM_pt_Lxybin4') 
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
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, p_{T}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################


    #####################################
    # dxy bins pt
    #####################################

    SI_DG_pt = getObject('plots_signal/th1fs.root', 'res_DG_pt_dxybin1') 
    SI_DGID_pt = getObject('plots_signal/th1fs.root', 'res_DGID_pt_dxybin1') 
    SI_GM_pt = getObject('plots_signal/th1fs.root', 'res_GM_pt_dxybin1') 
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
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, p_{T}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')

    #####################################

    SI_DG_pt = getObject('plots_signal/th1fs.root', 'res_DG_pt_dxybin2') 
    SI_DGID_pt = getObject('plots_signal/th1fs.root', 'res_DGID_pt_dxybin2') 
    SI_GM_pt = getObject('plots_signal/th1fs.root', 'res_GM_pt_dxybin2') 
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
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, p_{T}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')



    #####################################

    SI_DG_pt = getObject('plots_signal/th1fs.root', 'res_DG_pt_dxybin3') 
    SI_DGID_pt = getObject('plots_signal/th1fs.root', 'res_DGID_pt_dxybin3') 
    SI_GM_pt = getObject('plots_signal/th1fs.root', 'res_GM_pt_dxybin3') 
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
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, p_{T}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################

    SI_DG_pt = getObject('plots_signal/th1fs.root', 'res_DG_pt_dxybin4') 
    SI_DGID_pt = getObject('plots_signal/th1fs.root', 'res_DGID_pt_dxybin4') 
    SI_GM_pt = getObject('plots_signal/th1fs.root', 'res_GM_pt_dxybin4') 
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
    SI_allMU_pt_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, p_{T}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################


    #####################################
    # Lxy bins pt
    #####################################

    SI_DG_dxy = getObject('plots_signal/th1fs.root', 'res_DG_dxy_Lxybin1') 
    SI_DGID_dxy = getObject('plots_signal/th1fs.root', 'res_DGID_dxy_Lxybin1') 
    SI_GM_dxy = getObject('plots_signal/th1fs.root', 'res_GM_dxy_Lxybin1') 
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
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, d_{xy}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')

    #####################################

    SI_DG_dxy = getObject('plots_signal/th1fs.root', 'res_DG_dxy_Lxybin2') 
    SI_DGID_dxy = getObject('plots_signal/th1fs.root', 'res_DGID_dxy_Lxybin2') 
    SI_GM_dxy = getObject('plots_signal/th1fs.root', 'res_GM_dxy_Lxybin2') 
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
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, d_{xy}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')



    #####################################

    SI_DG_dxy = getObject('plots_signal/th1fs.root', 'res_DG_dxy_Lxybin3') 
    SI_DGID_dxy = getObject('plots_signal/th1fs.root', 'res_DGID_dxy_Lxybin3') 
    SI_GM_dxy = getObject('plots_signal/th1fs.root', 'res_GM_dxy_Lxybin3') 
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
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, d_{xy}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################

    SI_DG_dxy = getObject('plots_signal/th1fs.root', 'res_DG_dxy_Lxybin4') 
    SI_DGID_dxy = getObject('plots_signal/th1fs.root', 'res_DGID_dxy_Lxybin4') 
    SI_GM_dxy = getObject('plots_signal/th1fs.root', 'res_GM_dxy_Lxybin4') 
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
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, d_{xy}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################


    #####################################
    # dxy bins pt
    #####################################

    SI_DG_dxy = getObject('plots_signal/th1fs.root', 'res_DG_dxy_dxybin1') 
    SI_DGID_dxy = getObject('plots_signal/th1fs.root', 'res_DGID_dxy_dxybin1') 
    SI_GM_dxy = getObject('plots_signal/th1fs.root', 'res_GM_dxy_dxybin1') 
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
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, d_{xy}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')

    #####################################

    SI_DG_dxy = getObject('plots_signal/th1fs.root', 'res_DG_dxy_dxybin2') 
    SI_DGID_dxy = getObject('plots_signal/th1fs.root', 'res_DGID_dxy_dxybin2') 
    SI_GM_dxy = getObject('plots_signal/th1fs.root', 'res_GM_dxy_dxybin2') 
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
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, d_{xy}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')



    #####################################

    SI_DG_dxy = getObject('plots_signal/th1fs.root', 'res_DG_dxy_dxybin3') 
    SI_DGID_dxy = getObject('plots_signal/th1fs.root', 'res_DGID_dxy_dxybin3') 
    SI_GM_dxy = getObject('plots_signal/th1fs.root', 'res_GM_dxy_dxybin3') 
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
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, d_{xy}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################

    SI_DG_dxy = getObject('plots_signal/th1fs.root', 'res_DG_dxy_dxybin4') 
    SI_DGID_dxy = getObject('plots_signal/th1fs.root', 'res_DGID_dxy_dxybin4') 
    SI_GM_dxy = getObject('plots_signal/th1fs.root', 'res_GM_dxy_dxybin4') 
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
    SI_allMU_dxy_ = Canvas.Canvas("SI_allMU_dxy_dxybin4", 'png', 0.54, 0.67, 0.84, 0.78, 1)
    SI_allMU_dxy_.addHisto(SI_DG_dxy, 'HIST', 'Displaced Global', 'l', '', 1, 0)
    SI_allMU_dxy_.addHisto(SI_DGID_dxy, 'HIST,SAME', 'Displaced Global + ID', 'l', '', 1, 1)
    #SI_allMU_dxy_.addHisto(SI_GM_dxy, 'HIST,SAME', 'Standard Global', 'l', '', 1, 2)
    SI_allMU_dxy_.addLatex(0.85, 0.87, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', font = 62, size = 0.03, align = 31)
    SI_allMU_dxy_.addLatex(0.85, 0.82, '|#eta^{gen} < 2.4|, d_{xy}^{gen} > 10 GeV', size = 0.03, align = 31)
    SI_allMU_dxy_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fullresols_'+opts.tag+'/')


    #####################################








