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

    # ptmin > 10, eta cut 
    SI_DG_normChi2 = getObject('qass_signal_ptmin10/th1fs.root', 'qeff_DG_normChi2') 
    DY_DG_normChi2 = getObject('qass_DY2M_ptmin10/th1fs.root', 'qeff_DG_normChi2') 
    SI_DG_normChi2.SetTitle(';DG #chi^{2}/ndof;Fake rate')
    DY_DG_normChi2.SetTitle(';;')
    SI_DG_normChi2_ = Canvas.Canvas("SI_DG_normChi2", 'png', 0.57, 0.75, 0.87, 0.9, 1)
    SI_DG_normChi2_.addRate(DY_DG_normChi2, 'AP', '', 'p', r.kRed+2, 1, 0, marker = 24)
    SI_DG_normChi2_.addRate(SI_DG_normChi2, 'AP,SAME', '', 'p', r.kBlue+2, 1, 1, marker = 24)
    #SI_DG_normChi2_.addLatex(0.85, 0.85, 'Monte Carlo: H#rightarrowXX#rightarrow4l (All masses)', size = 0.03, align = 31)
    SI_DG_normChi2_.addLatex(0.9, 0.93, '|#eta^{DG} < 2.4|, p_{T}^{DG} > 10 GeV', size = 0.03, align = 31)
    SI_DG_normChi2_.save(0, 0, 0, '','', xlog = True, outputDir = WORKPATH + 'harvested_resols_'+opts.tag+'/')



