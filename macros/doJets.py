import ROOT as r
from   ROOT import gROOT, TCanvas, TFile, TGraphErrors, SetOwnership, TVector3
import math, sys, optparse, array, copy, os
import gc, inspect
import numpy as np

import include.Canvas as Canvas

####################################### CLASS DEFINITION #########################################



runningfile = os.path.abspath(__file__)
WORKPATH = ''
for level in runningfile.split('/')[:-1]:
    WORKPATH += level
    WORKPATH += '/'

print('runningfile: ' + runningfile)

##################################### FUNCTION DEFINITION ########################################


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
    parser.add_option('-f', '--filename', action='store', type=str, dest='filename', default='', help='Path to file')
    parser.add_option('-m', '--nmax', action='store', type=int, dest='nmax', default=0, help='Path to file')
    parser.add_option('--ptmin', action='store', type=float, dest='ptmin', default=0.0, help='ptmin')
    parser.add_option('--nhitmin', action='store', type=int, dest='nhitmin', default=0, help='ptmin')
    parser.add_option('--normChi2max', action='store', type=float, dest='normChi2max', default=0.0, help='ptmin')
    (opts, args) = parser.parse_args()

    outputPath =  WORKPATH + 'fakes_muons/' if not opts.tag else WORKPATH + 'fakes_' + opts.tag + '/'

    ##################################
    ####   Variable declaration   ####
    ##################################
    MAX_DELTAR = 0.2 



    #################################
    ####   TEfficiency binning   ####
    #################################
    ptres_bin = np.linspace(-1, 1, 100)
    sigmapt_sep = np.array([0.0, 0.4, 1.0])
    normChi2_sep = np.array([0.0, 5.0])
    sigmapt_bin = np.linspace(0, 5, 60)
    normChi2_bin = np.linspace(0, 15, 60)

    #############################
    ####   Book Histograms   ####
    #############################

    hist_nJet = r.TH1F("hist_nJet", ";Number of jets;Events", 20, 0, 80)
    hist_nGenJet = r.TH1F("hist_nGenJet", ";Number of jets;Events", 15, 0, 60)
    hist_jet_pt = r.TH1F("hist_jet_pt", ";Jet p_{T} (GeV);Jets", 100, 0, 300)
    hist_genjet_pt = r.TH1F("hist_genjet_pt", ";GenJet p_{T} (GeV);GenJets", 100, 0, 300)

    

    #########################
    ####   Load sample   ####
    #########################

    _sampleNames = (opts.filename).split(',')
    _tree = r.TChain('Events')
    for _name in _sampleNames:
        _tree.Add(_name)

    print("TTree with " + str(_tree.GetEntries()) + " entries")

    ###################################
    ####   Loop over tree events   ####
    ###################################

    for i in range(0, _tree.GetEntries()):

        _tree.GetEntry(i)
        if opts.nmax and i > opts.nmax: break

        if True:
            hist_nJet.Fill(_tree.nJet, _tree.wPU)
            hist_nGenJet.Fill(_tree.nGenJet, _tree.wPU)
     
        for pt in _tree.Jet_pt: hist_jet_pt.Fill(pt, _tree.wPU)
        for pt in _tree.GenJet_pt: hist_genjet_pt.Fill(pt, _tree.wPU)



    #### Write everything to a file:

    if not os.path.exists(WORKPATH + 'jets_'+opts.tag+'/'): os.makedirs(WORKPATH + 'jets_'+opts.tag+'/')
    outputFile = TFile(WORKPATH +'jets_'+ opts.tag + '/th1fs.root', 'RECREATE')

    hist_nJet.Write()
    hist_nGenJet.Write()
    hist_jet_pt.Write()
    hist_genjet_pt.Write()


    outputFile.Close()
