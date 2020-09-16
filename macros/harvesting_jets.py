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

    BCK_nJet = getObject('jets_DY2M/th1fs.root', 'hist_nJet')
    SI_nJet = getObject('jets_signal/th1fs.root', 'hist_nJet')
    BCK_nJet.Scale(1.0/BCK_nJet.Integral())
    SI_nJet.Scale(1.0/SI_nJet.Integral())
    BCK_nJet.SetLineWidth(2)
    SI_nJet.SetLineWidth(2)
    BCK_nJet.SetTitle(';Number of Jets;Normalized event yield')
    SI_nJet.SetTitle('')
    nJet_comp = Canvas.Canvas("nJet_comp", 'png', 0.35, 0.77, 0.67, 0.86, 1) 
    nJet_comp.addHisto(BCK_nJet, 'HIST', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'l', r.kRed+2, 1, 0)
    nJet_comp.addHisto(SI_nJet, 'HIST,SAME', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'l', r.kBlue+2, 1, 1)
    nJet_comp.saveRatio(1, 0, 1, '', SI_nJet, BCK_nJet, r_ymin=0, r_ymax=10, label ="Sig/Bkg", outputDir = 'harvested_jets/')


    BCK_nGenJet = getObject('jets_DY2M/th1fs.root', 'hist_nGenJet')
    SI_nGenJet = getObject('jets_signal/th1fs.root', 'hist_nGenJet')
    BCK_nGenJet.Scale(1.0/BCK_nGenJet.Integral())
    SI_nGenJet.Scale(1.0/SI_nGenJet.Integral())
    BCK_nGenJet.SetLineWidth(2)
    SI_nGenJet.SetLineWidth(2)
    BCK_nGenJet.SetTitle(';Number of GenJets;Normalized event yield')
    SI_nGenJet.SetTitle('')
    nGenJet_comp = Canvas.Canvas("nGenJet_comp", 'png', 0.35, 0.77, 0.67, 0.86, 1) 
    nGenJet_comp.addHisto(BCK_nGenJet, 'HIST', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'l', r.kRed+2, 1, 0)
    nGenJet_comp.addHisto(SI_nGenJet, 'HIST,SAME', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'l', r.kBlue+2, 1, 1)
    nGenJet_comp.saveRatio(1, 0, 1, '', SI_nGenJet, BCK_nGenJet, r_ymin=0, r_ymax=15, label ="Sig/Bkg", outputDir = 'harvested_jets/')


    BCK_jet_pt = getObject('jets_DY2M/th1fs.root', 'hist_jet_pt')
    SI_jet_pt = getObject('jets_signal/th1fs.root', 'hist_jet_pt')
    BCK_jet_pt.Scale(1.0/BCK_jet_pt.Integral())
    SI_jet_pt.Scale(1.0/SI_jet_pt.Integral())
    BCK_jet_pt.SetLineWidth(2)
    SI_jet_pt.SetLineWidth(2)
    BCK_jet_pt.SetTitle(';Jet p_{T} (GeV);Normalized event yield')
    SI_jet_pt.SetTitle('')
    jet_pt_comp = Canvas.Canvas("jet_pt_comp", 'png', 0.35, 0.77, 0.67, 0.86, 1) 
    jet_pt_comp.addHisto(BCK_jet_pt, 'HIST', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'l', r.kRed+2, 1, 0)
    jet_pt_comp.addHisto(SI_jet_pt, 'HIST,SAME', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'l', r.kBlue+2, 1, 1)
    jet_pt_comp.saveRatio(1, 0, 1, '', SI_jet_pt, BCK_jet_pt, r_ymin=0, r_ymax=200, label ="Sig/Bkg", outputDir = 'harvested_jets/')


    BCK_genjet_pt = getObject('jets_DY2M/th1fs.root', 'hist_genjet_pt')
    SI_genjet_pt = getObject('jets_signal/th1fs.root', 'hist_genjet_pt')
    BCK_genjet_pt.Scale(1.0/BCK_genjet_pt.Integral())
    SI_genjet_pt.Scale(1.0/SI_genjet_pt.Integral())
    BCK_genjet_pt.SetLineWidth(2)
    SI_genjet_pt.SetLineWidth(2)
    BCK_genjet_pt.SetTitle(';GenJet p_{T} (GeV);Normalized event yield')
    SI_genjet_pt.SetTitle('')
    genjet_pt_comp = Canvas.Canvas("genjet_pt_comp", 'png', 0.35, 0.77, 0.67, 0.86, 1) 
    genjet_pt_comp.addHisto(BCK_genjet_pt, 'HIST', 'Monte Carlo: Z/#gamma*#rightarrowl#bar{l} (DYJetsToLL_M-50)', 'l', r.kRed+2, 1, 0)
    genjet_pt_comp.addHisto(SI_genjet_pt, 'HIST,SAME', 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', 'l', r.kBlue+2, 1, 1)
    genjet_pt_comp.saveRatio(1, 0, 1, '', SI_genjet_pt, BCK_genjet_pt, r_ymin=0, r_ymax=200, label ="Sig/Bkg", outputDir = 'harvested_jets/')

