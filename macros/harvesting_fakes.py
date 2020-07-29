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

def doFakeStack(matched, unmatched, doOF = True, fakedown = False):

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
        Stack.Add(unmatched)    
        Stack.Add(matched)    
    else:
        Stack.Add(matched)    
        Stack.Add(unmatched)    

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

    # No cuts applied
    SI_matched_DG_pt = getObject('fakes_allSignals_v2/th1fs.root', 'matched_DG_pt')
    SI_unmatched_DG_pt = getObject('fakes_allSignals_v2/th1fs.root', 'unmatched_DG_pt')

    SI_DG_pt = doFakeStack(SI_matched_DG_pt, SI_unmatched_DG_pt, fakedown = True)

    SI_DG_pt_ = Canvas.Canvas("SI_DG_pt", 'png', 0.52, 0.81, 0.87, 0.9, 1) 
    SI_DG_pt_.addStack(SI_DG_pt, 'HIST', 1, 0)
    SI_DG_pt_.addLatex(0.41, 0.75, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 11)
    SI_DG_pt_.addLatex(0.41, 0.71, 'No DG cuts applied', size = 0.03, align = 11)
    SI_DG_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/', maxYnumbers = 4)

    #
    SI_fake_DG_pt = getObject('fakes_allSignals_v2/th1fs.root', 'total_DG_pt_clone')
    SI_fake_DG_pt.SetTitle(';DG p_{T} (GeV);DG Fake rate')
    SI_fake_DG_pt_ = Canvas.Canvas("SI_DG_pt", 'png', 0.41, 0.81, 0.75, 0.9, 1)
    SI_fake_DG_pt_.addRate(SI_fake_DG_pt, 'AP', 'Fake DG yield / Total DG yield', 'p', r.kRed+1, True, 0, marker = 24)
    SI_fake_DG_pt_.addLatex(0.41, 0.75, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 11)
    SI_fake_DG_pt_.addLatex(0.41, 0.71, 'No DG cuts applied', size = 0.03, align = 11)
    SI_fake_DG_pt_.save(1, 0, 0, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/')

    # ptmin10
    SI_matched_DG_nvalid = getObject('fakes_allSignals_ptmin15/th1fs.root', 'matched_DG_numberOfValidHits')
    SI_unmatched_DG_nvalid = getObject('fakes_allSignals_ptmin15/th1fs.root', 'unmatched_DG_numberOfValidHits')
    SI_DG_nvalid = doFakeStack(SI_matched_DG_nvalid, SI_unmatched_DG_nvalid)
    SI_DG_nvalid_ = Canvas.Canvas("SI_DG_nvalid", 'png', 0.52, 0.81, 0.87, 0.9, 1)
    SI_DG_nvalid_.addStack(SI_DG_nvalid, 'HIST', 1, 0)
    SI_DG_nvalid_.addLatex(0.41, 0.75, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 11)
    SI_DG_nvalid_.addLatex(0.41, 0.71, 'p_{T}^{DG} > 15 GeV', size = 0.03, align = 11)
    SI_DG_nvalid_.save(1, 0, 1, '','', outputDir = WORKPATH + 'harvested_fakes_'+opts.tag+'/')





