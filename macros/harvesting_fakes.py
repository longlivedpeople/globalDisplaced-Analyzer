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


def rebinAxis(eff, axis):

    totals = eff.GetTotalHistogram()
    passed = eff.GetPassedHistogram()
    totals_rebin = totals.Rebin(len(axis)-1, totals.GetName()+'_rebined', axis)
    passed_rebin = passed.Rebin(len(axis)-1, passed.GetName()+'_rebined', axis)
    neweff = r.TEfficiency(passed_rebin, totals_rebin)

    c1 = r.TCanvas()
    neweff.Draw('AP')
#    c1.SaveAs('Pruebita.png')

    return(neweff)



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



    #############################################
    ####   Number of hits in muon chambers   ####
    #############################################

    nMU_bin = np.linspace(0, 15, 16)

    # nMU spectra in signal in stacked histogram
    matched_DG_nMU = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi10_nOut10_nTOT20/th1fs.root', 'matched_DG_nMU')
    unmatched_DG_nMU = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi10_nOut10_nTOT20/th1fs.root', 'unmatched_DG_nMU')

    matched_DG_nMU = matched_DG_nMU.Rebin(len(nMU_bin)-1, matched_DG_nMU.GetName() + '_rebined', nMU_bin)
    unmatched_DG_nMU = unmatched_DG_nMU.Rebin(len(nMU_bin)-1, matched_DG_nMU.GetName() + '_rebined', nMU_bin)

    matched_DG_nMU.SetTitle(';Number of hits in Muon Chambers; dGlobal yield')
    DG_nMU = doFakeStack(matched_DG_nMU, unmatched_DG_nMU, fakedown = False)
    DG_nMU.SetMaximum(100.0*DG_nMU.GetMaximum())
    DG_nMU.SetMinimum(0.1)
    DG_nMU_ = Canvas.Canvas("nMU_optimization", 'png', 0.52, 0.81, 0.87, 0.9, 1) 
    DG_nMU_.addStack(DG_nMU, 'HIST', 1, 0)
    DG_nMU_.addLatex(0.41, 0.75, 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 11, font = 62)
    DG_nMU_.addLatex(0.41, 0.71, 'TBD', size = 0.03, align = 11)
    DG_nMU_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', maxYnumbers = 4)

    # Fake rate vs nMU
    fake_DG_nMU = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi10_nOut10_nTOT20/th1fs.root', 'total_DG_nMU_clone')
    fake_DG_nMU.SetTitle(';Number of hits in Muon Chambers; Fake fraction')
    fake_DG_nMU = rebinAxis(fake_DG_nMU, nMU_bin)

    fake_DG_nMU_ = Canvas.Canvas("nMU_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_nMU_.addRate(fake_DG_nMU, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_nMU_.addLatex(0.85, 0.85, 'p_{T} > 10 GeV', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.85, 0.81, '|#eta| < 2.4', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.85, 0.77, '#sigma_{p_{T}}/p_{T} < 0.3', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.85, 0.73, '#chi^{2}/ndof < 10', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.85, 0.69, 'N outer tracker hits >= 10', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.85, 0.65, 'N total hits >= 20', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_nMU_.addLine(3.0, 0, 3.0, 1.2, r.kBlue, thickness = 1)
    fake_DG_nMU_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/')

    # Fake rate vs nMU
    fake_DG_nMU = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi7p5_nOut10_nTOT20/th1fs.root', 'total_DG_nMU_clone')
    fake_DG_nMU.SetTitle(';Number of hits in Muon Chambers; Fake fraction')
    fake_DG_nMU = rebinAxis(fake_DG_nMU, nMU_bin)

    fake_DG_nMU_ = Canvas.Canvas("nMU_chi7p5_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_nMU_.addRate(fake_DG_nMU, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_nMU_.addLatex(0.85, 0.85, 'p_{T} > 10 GeV', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.85, 0.81, '|#eta| < 2.4', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.85, 0.77, '#sigma_{p_{T}}/p_{T} < 0.3', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.85, 0.73, '#chi^{2}/ndof < 7.5', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.85, 0.69, 'N outer tracker hits >= 10', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.85, 0.65, 'N total hits >= 20', size = 0.03, align = 31)
    fake_DG_nMU_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_nMU_.addLine(3.0, 0, 3.0, 1.2, r.kBlue, thickness = 1)
    fake_DG_nMU_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/')


    ##########################################
    ####   Number of outer tracker hits   ####
    ##########################################

    nOutTR_bin = np.linspace(0, 32, 33)

    # nOutTR spectra in signal in stacked histogram
    matched_DG_nOutTR = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi10_nMU3_nTOT20/th1fs.root', 'matched_DG_nOutTR')
    unmatched_DG_nOutTR = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi10_nMU3_nTOT20/th1fs.root', 'unmatched_DG_nOutTR')

    matched_DG_nOutTR = matched_DG_nOutTR.Rebin(len(nOutTR_bin)-1, matched_DG_nOutTR.GetName() + '_rebined', nOutTR_bin)
    unmatched_DG_nOutTR = unmatched_DG_nOutTR.Rebin(len(nOutTR_bin)-1, matched_DG_nOutTR.GetName() + '_rebined', nOutTR_bin)

    matched_DG_nOutTR.SetTitle(';Number of hits in outer tracker; dGlobal yield')
    DG_nOutTR = doFakeStack(matched_DG_nOutTR, unmatched_DG_nOutTR, fakedown = False)
    DG_nOutTR.SetMaximum(100.0*DG_nOutTR.GetMaximum())
    DG_nOutTR.SetMinimum(0.1)
    DG_nOutTR_ = Canvas.Canvas("nOutTR_optimization", 'png', 0.52, 0.81, 0.87, 0.9, 1) 
    DG_nOutTR_.addStack(DG_nOutTR, 'HIST', 1, 0)
    DG_nOutTR_.addLatex(0.41, 0.75, 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 11, font = 62)
    DG_nOutTR_.addLatex(0.41, 0.71, 'TBD', size = 0.03, align = 11)
    DG_nOutTR_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', maxYnumbers = 4)

    # Fake rate vs nOutTR
    fake_DG_nOutTR = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi10_nMU3_nTOT20/th1fs.root', 'total_DG_nOutTR_clone')
    fake_DG_nOutTR.SetTitle(';Number of hits in outer tracker; Fake fraction')
    fake_DG_nOutTR = rebinAxis(fake_DG_nOutTR, nOutTR_bin)

    fake_DG_nOutTR_ = Canvas.Canvas("nOutTR_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_nOutTR_.addRate(fake_DG_nOutTR, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_nOutTR_.addLatex(0.85, 0.85, 'p_{T} > 10 GeV', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.85, 0.81, '|#eta| < 2.4', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.85, 0.77, '#sigma_{p_{T}}/p_{T} < 0.3', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.85, 0.73, '#chi^{2}/ndof < 10', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.85, 0.69, 'N muon hits >= 3', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.85, 0.65, 'N total hits >= 20', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_nOutTR_.addLine(10.0, 0, 10.0, 1.2, r.kBlue, thickness = 1)
    fake_DG_nOutTR_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/')


    # Fake rate vs nOutTR (chi 7.5)
    fake_DG_nOutTR = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi7p5_nMU3_nTOT20/th1fs.root', 'total_DG_nOutTR_clone')
    fake_DG_nOutTR.SetTitle(';Number of hits in outer tracker; Fake fraction')
    fake_DG_nOutTR = rebinAxis(fake_DG_nOutTR, nOutTR_bin)

    fake_DG_nOutTR_ = Canvas.Canvas("nOutTR_chi7p5_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_nOutTR_.addRate(fake_DG_nOutTR, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_nOutTR_.addLatex(0.85, 0.85, 'p_{T} > 10 GeV', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.85, 0.81, '|#eta| < 2.4', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.85, 0.77, '#sigma_{p_{T}}/p_{T} < 0.3', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.85, 0.73, '#chi^{2}/ndof < 7.5', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.85, 0.69, 'N muon hits >= 3', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.85, 0.65, 'N total hits >= 20', size = 0.03, align = 31)
    fake_DG_nOutTR_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_nOutTR_.addLine(10.0, 0, 10.0, 1.2, r.kBlue, thickness = 1)
    fake_DG_nOutTR_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/')



    ##################################
    ####   Number of total hits   ####
    ##################################

    numberOfValidHits_bin = np.linspace(0, 74, 75)

    # numberOfValidHits spectra in signal in stacked histogram
    matched_DG_numberOfValidHits = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi10_nMU3_nOut10/th1fs.root', 'matched_DG_numberOfValidHits')
    unmatched_DG_numberOfValidHits = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi10_nMU3_nOut10/th1fs.root', 'unmatched_DG_numberOfValidHits')

    matched_DG_numberOfValidHits = matched_DG_numberOfValidHits.Rebin(len(numberOfValidHits_bin)-1, matched_DG_numberOfValidHits.GetName() + '_rebined', numberOfValidHits_bin)
    unmatched_DG_numberOfValidHits = unmatched_DG_numberOfValidHits.Rebin(len(numberOfValidHits_bin)-1, matched_DG_numberOfValidHits.GetName() + '_rebined', numberOfValidHits_bin)

    matched_DG_numberOfValidHits.SetTitle(';Number of total hits; dGlobal yield')
    DG_numberOfValidHits = doFakeStack(matched_DG_numberOfValidHits, unmatched_DG_numberOfValidHits, fakedown = False)
    DG_numberOfValidHits.SetMaximum(100.0*DG_numberOfValidHits.GetMaximum())
    DG_numberOfValidHits.SetMinimum(0.1)
    DG_numberOfValidHits_ = Canvas.Canvas("numberOfValidHits_optimization", 'png', 0.52, 0.81, 0.87, 0.9, 1) 
    DG_numberOfValidHits_.addStack(DG_numberOfValidHits, 'HIST', 1, 0)
    DG_numberOfValidHits_.addLatex(0.41, 0.75, 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 11, font = 62)
    DG_numberOfValidHits_.addLatex(0.41, 0.71, 'TBD', size = 0.03, align = 11)
    DG_numberOfValidHits_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', maxYnumbers = 4)

    # Fake rate vs numberOfValidHits
    fake_DG_numberOfValidHits = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi10_nMU3_nOut10/th1fs.root', 'total_DG_numberOfValidHits_clone')
    fake_DG_numberOfValidHits.SetTitle(';Number of total hits; Fake fraction')
    fake_DG_numberOfValidHits = rebinAxis(fake_DG_numberOfValidHits, numberOfValidHits_bin)

    fake_DG_numberOfValidHits_ = Canvas.Canvas("numberOfValidHits_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_numberOfValidHits_.addRate(fake_DG_numberOfValidHits, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.85, 'p_{T} > 10 GeV', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.81, '|#eta| < 2.4', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.77, '#sigma_{p_{T}}/p_{T} < 0.3', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.73, '#chi^{2}/ndof < 10', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.65, 'N outer tracker hits >= 10', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.69, 'N muon hits >= 3', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLine(20.0, 0, 20.0, 1.2, r.kBlue, thickness = 1)
    fake_DG_numberOfValidHits_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_numberOfValidHits_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/')

    # Fake rate vs numberOfValidHits (chi 7.5)
    fake_DG_numberOfValidHits = getObject('fakes_Drell-Yan_pt_eta_sigmapt_chi7p5_nMU3_nOut10/th1fs.root', 'total_DG_numberOfValidHits_clone')
    fake_DG_numberOfValidHits.SetTitle(';Number of total hits; Fake fraction')
    fake_DG_numberOfValidHits = rebinAxis(fake_DG_numberOfValidHits, numberOfValidHits_bin)

    fake_DG_numberOfValidHits_ = Canvas.Canvas("numberOfValidHits_chi7p5_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_numberOfValidHits_.addRate(fake_DG_numberOfValidHits, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.85, 'p_{T} > 10 GeV', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.81, '|#eta| < 2.4', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.77, '#sigma_{p_{T}}/p_{T} < 0.3', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.73, '#chi^{2}/ndof < 7.5', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.65, 'N outer tracker hits >= 10', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLatex(0.85, 0.69, 'N muon hits >= 3', size = 0.03, align = 31)
    fake_DG_numberOfValidHits_.addLine(20.0, 0, 20.0, 1.2, r.kBlue, thickness = 1)
    fake_DG_numberOfValidHits_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_numberOfValidHits_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/')



    ####################################
    ####   Normalized chi squared   ####
    ####################################

    normChi2_bin = np.linspace(0, 32, 33)

    # normChi2 spectra in signal in stacked histogram
    matched_DG_normChi2 = getObject('fakes_Drell-Yan_pt_eta_sigmapt_nMU3_nOut10_nTOT20/th1fs.root', 'matched_DG_normChi2')
    unmatched_DG_normChi2 = getObject('fakes_Drell-Yan_pt_eta_sigmapt_nMU3_nOut10_nTOT20/th1fs.root', 'unmatched_DG_normChi2')

    #matched_DG_normChi2 = matched_DG_normChi2.Rebin(len(normChi2_bin)-1, matched_DG_normChi2.GetName() + '_rebined', normChi2_bin)
    #unmatched_DG_normChi2 = unmatched_DG_normChi2.Rebin(len(normChi2_bin)-1, matched_DG_normChi2.GetName() + '_rebined', normChi2_bin)

    matched_DG_normChi2.SetTitle(';dGlobal #chi^{2}/ndof; dGlobal yield')
    DG_normChi2 = doFakeStack(matched_DG_normChi2, unmatched_DG_normChi2, fakedown = False)
    DG_normChi2.SetMaximum(100.0*DG_normChi2.GetMaximum())
    DG_normChi2.SetMinimum(0.1)
    DG_normChi2_ = Canvas.Canvas("normChi2_optimization", 'png', 0.52, 0.81, 0.87, 0.9, 1) 
    DG_normChi2_.addStack(DG_normChi2, 'HIST', 1, 0)
    DG_normChi2_.addLatex(0.41, 0.75, 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 11, font = 62)
    DG_normChi2_.addLatex(0.41, 0.71, 'TBD', size = 0.03, align = 11)
    DG_normChi2_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', maxYnumbers = 4)

    # Fake rate vs normChi2
    fake_DG_normChi2 = getObject('fakes_Drell-Yan_pt_eta_sigmapt_nMU3_nOut10_nTOT20/th1fs.root', 'total_DG_normChi2_clone')
    fake_DG_normChi2.SetTitle(';dGlobal #chi^{2}/ndof; Fake fraction')
    #fake_DG_normChi2 = rebinAxis(fake_DG_normChi2, normChi2_bin)

    fake_DG_normChi2_ = Canvas.Canvas("normChi2_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_normChi2_.addRate(fake_DG_normChi2, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_normChi2_.addLatex(0.85, 0.85, 'p_{T} > 10 GeV', size = 0.03, align = 31)
    fake_DG_normChi2_.addLatex(0.85, 0.81, '|#eta| < 2.4', size = 0.03, align = 31)
    fake_DG_normChi2_.addLatex(0.85, 0.77, '#sigma_{p_{T}}/p_{T} < 0.3', size = 0.03, align = 31)
    fake_DG_normChi2_.addLatex(0.85, 0.73, 'N outer tracker hits >= 10', size = 0.03, align = 31)
    fake_DG_normChi2_.addLatex(0.85, 0.69, 'N muon hits >= 3', size = 0.03, align = 31)
    fake_DG_normChi2_.addLatex(0.85, 0.65, 'N total hits >= 20', size = 0.03, align = 31)
    fake_DG_normChi2_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_normChi2_.addLine(7.5, 0, 7.5, 1.2, r.kBlue, thickness = 1)
    fake_DG_normChi2_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/')


    #########################################
    ####   Reconstructed pT resolution   ####
    #########################################

    ptSig_bin = np.logspace(-3, 2, 50)
    for n in range(0, len(ptSig_bin)): print(n, ptSig_bin[n])
    ptSig_bin = np.concatenate((ptSig_bin[:25], ptSig_bin[[28]], ptSig_bin[[34]], ptSig_bin[[-1]]))

    # ptSig spectra in signal in stacked histogram
    matched_DG_ptSig = getObject('fakes_Drell-Yan_pt_eta_chi10_nMU3_nOut10_nTOT20/th1fs.root', 'matched_DG_ptSig')
    unmatched_DG_ptSig = getObject('fakes_Drell-Yan_pt_eta_chi10_nMU3_nOut10_nTOT20/th1fs.root', 'unmatched_DG_ptSig')

    #matched_DG_ptSig = matched_DG_ptSig.Rebin(len(ptSig_bin)-1, matched_DG_ptSig.GetName() + '_rebined', ptSig_bin)
    #unmatched_DG_ptSig = unmatched_DG_ptSig.Rebin(len(ptSig_bin)-1, matched_DG_ptSig.GetName() + '_rebined', ptSig_bin)

    matched_DG_ptSig.SetTitle(';dGlobal #sigma_{p_{T}}/p_{T}; dGlobal yield')
    DG_ptSig = doFakeStack(matched_DG_ptSig, unmatched_DG_ptSig, fakedown = False)
    DG_ptSig.SetMaximum(100.0*DG_ptSig.GetMaximum())
    DG_ptSig.SetMinimum(0.1)
    DG_ptSig_ = Canvas.Canvas("ptSig_optimization", 'png', 0.52, 0.81, 0.87, 0.9, 1) 
    DG_ptSig_.addStack(DG_ptSig, 'HIST', 1, 0)
    DG_ptSig_.addLatex(0.41, 0.75, 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 11, font = 62)
    DG_ptSig_.addLatex(0.41, 0.71, 'TBD', size = 0.03, align = 11)
    DG_ptSig_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', xlog = True)

    # Fake rate vs ptSig
    fake_DG_ptSig = getObject('fakes_Drell-Yan_pt_eta_chi10_nMU3_nOut10_nTOT20/th1fs.root', 'total_DG_ptSig_clone')
    fake_DG_ptSig.SetTitle(';dGlobal #sigma_{p_{T}}/p_{T}; Fake fraction')
    fake_DG_ptSig = rebinAxis(fake_DG_ptSig, ptSig_bin)

    fake_DG_ptSig_ = Canvas.Canvas("ptSig_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_ptSig_.addRate(fake_DG_ptSig, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_ptSig_.addLatex(0.85, 0.85, 'p_{T} > 10 GeV', size = 0.03, align = 31)
    fake_DG_ptSig_.addLatex(0.85, 0.81, '|#eta| < 2.4', size = 0.03, align = 31)
    fake_DG_ptSig_.addLatex(0.85, 0.77, '#chi^{2}/ndof < 10', size = 0.03, align = 31)
    fake_DG_ptSig_.addLatex(0.85, 0.73, 'N outer tracker hits >= 10', size = 0.03, align = 31)
    fake_DG_ptSig_.addLatex(0.85, 0.69, 'N muon hits >= 3', size = 0.03, align = 31)
    fake_DG_ptSig_.addLatex(0.85, 0.65, 'N total hits >= 20', size = 0.03, align = 31)
    fake_DG_ptSig_.addLine(0.3, 0, 0.3, 1.2, r.kBlue, thickness = 1)
    fake_DG_ptSig_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_ptSig_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', xlog = True)

    # Fake rate vs ptSig (7.5 chi)
    fake_DG_ptSig = getObject('fakes_Drell-Yan_pt_eta_chi7p5_nMU3_nOut10_nTOT20/th1fs.root', 'total_DG_ptSig_clone')
    fake_DG_ptSig.SetTitle(';dGlobal #sigma_{p_{T}}/p_{T}; Fake fraction')
    fake_DG_ptSig = rebinAxis(fake_DG_ptSig, ptSig_bin)

    fake_DG_ptSig_ = Canvas.Canvas("ptSig_chi7p5_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_ptSig_.addRate(fake_DG_ptSig, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_ptSig_.addLatex(0.85, 0.85, 'p_{T} > 10 GeV', size = 0.03, align = 31)
    fake_DG_ptSig_.addLatex(0.85, 0.81, '|#eta| < 2.4', size = 0.03, align = 31)
    fake_DG_ptSig_.addLatex(0.85, 0.77, '#chi^{2}/ndof < 7.5', size = 0.03, align = 31)
    fake_DG_ptSig_.addLatex(0.85, 0.73, 'N outer tracker hits >= 10', size = 0.03, align = 31)
    fake_DG_ptSig_.addLatex(0.85, 0.69, 'N muon hits >= 3', size = 0.03, align = 31)
    fake_DG_ptSig_.addLatex(0.85, 0.65, 'N total hits >= 20', size = 0.03, align = 31)
    fake_DG_ptSig_.addLine(0.3, 0, 0.3, 1.2, r.kBlue, thickness = 1)
    fake_DG_ptSig_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_ptSig_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', xlog = True)



    # ----> Total Fake rate vs pt (7.5 chi)
    fake_DG_pt = getObject('fakes_Drell-Yan_eta_sigmapt_chi7p5_nMU3_nOut10_nTOT20/th1fs.root', 'total_DG_pt_clone')
    fake_DG_pt.SetTitle(';dGlobal p_{T}; Fake fraction')
    #fake_DG_pt = rebinAxis(fake_DG_pt, pt_bin)

    fake_DG_pt_ = Canvas.Canvas("pt_chi7p5_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_pt_.addRate(fake_DG_pt, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_pt_.addLatex(0.85, 0.85, '|#eta| < 2.4', size = 0.03, align = 31)
    fake_DG_pt_.addLatex(0.85, 0.81, '#sigma_{p_{T}}/p_{T} < 0.3', size = 0.03, align = 31)
    fake_DG_pt_.addLatex(0.85, 0.77, '#chi^{2}/ndof < 7.5', size = 0.03, align = 31)
    fake_DG_pt_.addLatex(0.85, 0.73, 'N outer tracker hits >= 10', size = 0.03, align = 31)
    fake_DG_pt_.addLatex(0.85, 0.69, 'N muon hits >= 3', size = 0.03, align = 31)
    fake_DG_pt_.addLatex(0.85, 0.65, 'N total hits >= 20', size = 0.03, align = 31)
    fake_DG_pt_.addLine(10.0, 0, 10.0, 1.2, r.kBlue, thickness = 1)
    fake_DG_pt_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_pt_.addLine(10.0, 0, 10.0, 1.2, r.kBlue, thickness = 1)
    fake_DG_pt_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', xlog = False)


    # ----> Total Fake rate vs eta (7.5 chi)
    fake_DG_eta = getObject('fakes_Drell-Yan_pt_sigmapt_chi7p5_nMU3_nOut10_nTOT20/th1fs.root', 'total_DG_eta_clone')
    fake_DG_eta.SetTitle(';dGlobal #eta; Fake fraction')
    #fake_DG_eta = rebinAxis(fake_DG_eta, eta_bin)

    fake_DG_eta_ = Canvas.Canvas("eta_chi7p5_fake", 'png', 0.15, 0.81, 0.5, 0.9, 1)
    fake_DG_eta_.addRate(fake_DG_eta, 'AP', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'p', r.kRed, True, 0, marker = 24)
    fake_DG_eta_.addLatex(0.85, 0.85, 'p_T > 10 GeV', size = 0.03, align = 31)
    fake_DG_eta_.addLatex(0.85, 0.81, '#sigma_{p_{T}}/p_{T} < 0.3', size = 0.03, align = 31)
    fake_DG_eta_.addLatex(0.85, 0.77, '#chi^{2}/ndof < 7.5', size = 0.03, align = 31)
    fake_DG_eta_.addLatex(0.85, 0.73, 'N outer tracker hits >= 10', size = 0.03, align = 31)
    fake_DG_eta_.addLatex(0.85, 0.69, 'N muon hits >= 3', size = 0.03, align = 31)
    fake_DG_eta_.addLatex(0.85, 0.65, 'N total hits >= 20', size = 0.03, align = 31)
    fake_DG_eta_.addLatex(0.9, 0.93, 'Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', size = 0.03, align = 31, font = 62)
    fake_DG_eta_.addLine(2.4, 0, 2.4, 1.2, r.kBlue, thickness = 1)
    fake_DG_eta_.addLine(-2.4, 0, -2.4, 1.2, r.kBlue, thickness = 1)
    fake_DG_eta_.save(0, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', xlog = False)

