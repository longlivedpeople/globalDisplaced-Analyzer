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
    (opts, args) = parser.parse_args()


    ##################################
    ####   Variable declaration   ####
    ##################################
    MAX_DELTAR = 0.2 



    #################################
    ####   TEfficiency binning   ####
    #################################
    #Lxy_bin = np.array([0.0, 0.025, 0.5, 1.0, 2.0, 4.0, 8.0, 12.0, 16.0, 20., 30., 40., 50., 60., 70., 90., 110.0])
    #Lxy_bin = np.linspace(0.0, 110.0, 51)
    Lxy_bin = np.linspace(0.0, 110.0, 100)
    Lxy_profbin = np.array([0.0, 1.0, 5.0, 10.0, 15.0, 20.0, 30.0, 40.0, 60.0, 80.0, 100.0])
    dxy_bin = np.linspace(0.0, 60.0, 30)
    Lxy_logbin = np.logspace(0.0, 3.0, 101)
    #pt_bin = np.concatenate((np.linspace(0, 125, 15), np.array([150, 175, 200, 250, 300, 400, 500])))
    pt_bin = np.linspace(0.0, 300.0, 80) # 100, 60 for DY
    eta_bin = np.linspace(-5.0, 5.0, 40)
    Lxy_sep = np.array([0.0, 1.0, 20.0, 110.0])
    dxy_sep = np.array([0.0, 1.0, 20.0, 110.0])
    

    ###############################
    ####   Book TH1F objects   ####
    ###############################
    
    #
    # -- genMu histograms
    #
    total_genMu_pt = r.TH1F("total_genMu_pt", ";Generated #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    recoGM_genMu_pt = r.TH1F("recoGM_genMu_pt", ";Generated #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)
    recoDG_genMu_pt = r.TH1F("recoDG_genMu_pt", ";Generated #mu p_{T} (GeV);Muons", len(pt_bin)-1, pt_bin)

    total_genMu_eta = r.TH1F("total_genMu_eta", ";Generated #mu #eta (GeV);Muons", len(eta_bin)-1, eta_bin)
    recoGM_genMu_eta = r.TH1F("recoGM_genMu_eta", ";Generated #mu #eta (GeV);Muons", len(eta_bin)-1, eta_bin)
    recoDG_genMu_eta = r.TH1F("recoDG_genMu_eta", ";Generated #mu #eta (GeV);Muons", len(eta_bin)-1, eta_bin)

    total_genMu_Lxy = r.TH1F("total_genMu_Lxy", ";Generated #mu decay radius r (cm);Muons", len(Lxy_bin)-1, Lxy_bin)
    recoGM_genMu_Lxy = r.TH1F("recoGM_genMu_Lxy", ";Generated #mu decay radius r (cm);Muons", len(Lxy_bin)-1, Lxy_bin)
    recoDG_genMu_Lxy = r.TH1F("recoDG_genMu_Lxy", ";Generated #mu decay radius r (cm);Muons", len(Lxy_bin)-1, Lxy_bin)



    ######################################
    ####   Book TEfficiency objects   ####
    ######################################

    eff_GM_pt_Lxybin1 = r.TEfficiency("eff_GM_pt_Lxybin1", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_GM_pt_Lxybin2 = r.TEfficiency("eff_GM_pt_Lxybin2", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_GM_pt_Lxybin3 = r.TEfficiency("eff_GM_pt_Lxybin3", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)

    eff_DG_pt_Lxybin1 = r.TEfficiency("eff_DG_pt_Lxybin1", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DG_pt_Lxybin2 = r.TEfficiency("eff_DG_pt_Lxybin2", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DG_pt_Lxybin3 = r.TEfficiency("eff_DG_pt_Lxybin3", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)

    ######################################
    eff_GM_pt_dxybin1 = r.TEfficiency("eff_GM_pt_dxybin1", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_GM_pt_dxybin2 = r.TEfficiency("eff_GM_pt_dxybin2", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_GM_pt_dxybin3 = r.TEfficiency("eff_GM_pt_dxybin3", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)

    eff_DG_pt_dxybin1 = r.TEfficiency("eff_DG_pt_dxybin1", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DG_pt_dxybin2 = r.TEfficiency("eff_DG_pt_dxybin2", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)
    eff_DG_pt_dxybin3 = r.TEfficiency("eff_DG_pt_dxybin3", ";Generated muon p_{T} (GeV);Efficiency", len(pt_bin)-1, pt_bin)



    #########################
    ####   Load sample   ####
    #########################
    _sampleName = opts.filename
    _file = TFile(_sampleName)
    _tree = _file.Get("Events")
    print("TTree with " + str(_tree.GetEntries()) + " entries")


    ###################################
    ####   Loop over tree events   ####
    ###################################

    for i in range(0, _tree.GetEntries()):

        _tree.GetEntry(i)

        for j in range(0, _tree.ngenMu):

            if not _tree.genMu_isPromptFinalState[j]: continue

            pt    = _tree.genMu_pt[j]
            eta    = _tree.genMu_eta[j]
            phi    = _tree.genMu_phi[j]
            vx    = _tree.genMu_vx[j]
            vy    = _tree.genMu_vy[j]
            dxy    = _tree.genMu_dxy[j]
            dz    = _tree.genMu_dz[j]
            Lxy = math.sqrt(vx**2 + vy**2)

            if pt < 10: continue
            #if abs(eta) > 2.0: continue

            l = TVector3()
            l.SetPtEtaPhi(pt, eta, phi)

            total_genMu_pt.Fill(pt)
            total_genMu_eta.Fill(eta)
            total_genMu_Lxy.Fill(Lxy)

            #
            # -- GBs
            #
            deltaR = 9999.0
            index = -9
            for k in range(0, _tree.nGM):
                re = TVector3()
                re.SetPtEtaPhi(_tree.GM_pt[k], _tree.GM_eta[k], _tree.GM_phi[k])
                if l.DeltaR(re) < deltaR:
                    deltaR = l.DeltaR(re)
                    index = k

            if deltaR < MAX_DELTAR:

                recoGM_genMu_pt.Fill(pt)
                recoGM_genMu_eta.Fill(eta)
                recoGM_genMu_Lxy.Fill(Lxy)

                if Lxy < Lxy_sep[1]:
                    eff_GM_pt_Lxybin1.Fill(True, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[2]:
                    eff_GM_pt_Lxybin2.Fill(True, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[3]:
                    eff_GM_pt_Lxybin3.Fill(True, pt)

                if dxy < dxy_sep[1]:
                    eff_GM_pt_dxybin1.Fill(True, pt)
                elif dxy > dxy_sep[1] and dxy < dxy_sep[2]:
                    eff_GM_pt_dxybin2.Fill(True, pt)
                elif dxy > dxy_sep[1] and dxy < dxy_sep[3]:
                    eff_GM_pt_dxybin3.Fill(True, pt)

            else:

                if Lxy < Lxy_sep[1]:
                    eff_GM_pt_Lxybin1.Fill(False, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[2]:
                    eff_GM_pt_Lxybin2.Fill(False, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[3]:
                    eff_GM_pt_Lxybin3.Fill(False, pt)

                if dxy < dxy_sep[1]:
                    eff_GM_pt_dxybin1.Fill(False, pt)
                elif dxy > dxy_sep[1] and dxy < dxy_sep[2]:
                    eff_GM_pt_dxybin2.Fill(False, pt)
                elif dxy > dxy_sep[1] and dxy < dxy_sep[3]:
                    eff_GM_pt_dxybin3.Fill(False, pt)


            #
            # -- DGs
            #
            deltaR = 9999.0
            index = -9
            for k in range(0, _tree.nDG):
                re = TVector3()
                re.SetPtEtaPhi(_tree.DG_pt[k], _tree.DG_eta[k], _tree.DG_phi[k])
                if l.DeltaR(re) < deltaR:
                    deltaR = l.DeltaR(re)
                    index = k

            if deltaR < MAX_DELTAR:

                recoDG_genMu_pt.Fill(pt)
                recoDG_genMu_eta.Fill(eta)
                recoDG_genMu_Lxy.Fill(Lxy)

                if Lxy < Lxy_sep[1]:
                    eff_DG_pt_Lxybin1.Fill(True, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[2]:
                    eff_DG_pt_Lxybin2.Fill(True, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[3]:
                    eff_DG_pt_Lxybin3.Fill(True, pt)

                if dxy < dxy_sep[1]:
                    eff_DG_pt_dxybin1.Fill(True, pt)
                elif dxy > dxy_sep[1] and dxy < dxy_sep[2]:
                    eff_DG_pt_dxybin2.Fill(True, pt)
                elif dxy > dxy_sep[1] and dxy < dxy_sep[3]:
                    eff_DG_pt_dxybin3.Fill(True, pt)

            else:

                if Lxy < Lxy_sep[1]:
                    eff_DG_pt_Lxybin1.Fill(False, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[2]:
                    eff_DG_pt_Lxybin2.Fill(False, pt)
                elif Lxy > Lxy_sep[1] and Lxy < Lxy_sep[3]:
                    eff_DG_pt_Lxybin3.Fill(False, pt)

                if dxy < dxy_sep[1]:
                    eff_DG_pt_dxybin1.Fill(False, pt)
                elif dxy > dxy_sep[1] and dxy < dxy_sep[2]:
                    eff_DG_pt_dxybin2.Fill(False, pt)
                elif dxy > dxy_sep[1] and dxy < dxy_sep[3]:
                    eff_DG_pt_dxybin3.Fill(False, pt)


    #####################################
    ####   Construct TEfficiencies   ####
    #####################################
    eff_GM_pt = r.TEfficiency(recoGM_genMu_pt, total_genMu_pt)
    eff_GM_pt.SetTitle('eff_GM_pt;'+total_genMu_pt.GetXaxis().GetTitle()+'; Efficiency')
    eff_GM_eta = r.TEfficiency(recoGM_genMu_eta, total_genMu_eta)
    eff_GM_eta.SetTitle('eff_GM_eta;'+total_genMu_eta.GetXaxis().GetTitle()+'; Efficiency')
    eff_GM_Lxy = r.TEfficiency(recoGM_genMu_Lxy, total_genMu_Lxy)
    eff_GM_Lxy.SetTitle('eff_GM_Lxy;'+total_genMu_Lxy.GetXaxis().GetTitle()+'; Efficiency')

    eff_DG_pt = r.TEfficiency(recoDG_genMu_pt, total_genMu_pt)
    eff_DG_pt.SetTitle('eff_DG_pt;'+total_genMu_pt.GetXaxis().GetTitle()+'; Efficiency')
    eff_DG_eta = r.TEfficiency(recoDG_genMu_eta, total_genMu_eta)
    eff_DG_eta.SetTitle('eff_DG_eta;'+total_genMu_eta.GetXaxis().GetTitle()+'; Efficiency')
    eff_DG_Lxy = r.TEfficiency(recoDG_genMu_Lxy, total_genMu_Lxy)
    eff_DG_Lxy.SetTitle('eff_DG_Lxy;'+total_genMu_Lxy.GetXaxis().GetTitle()+'; Efficiency')


    if not os.path.exists(WORKPATH + 'plots_'+opts.tag+'/'): os.makedirs(WORKPATH + 'plots_'+opts.tag+'/')
    outputFile = TFile(WORKPATH +'plots_'+ opts.tag + '/th1fs.root', 'RECREATE')



    #### Write everything to use later:
    total_genMu_pt.Write()
    recoGM_genMu_pt.Write()
    recoDG_genMu_pt.Write()
    eff_GM_pt.Write()
    eff_DG_pt.Write()
    eff_GM_pt_Lxybin1.Write()
    eff_GM_pt_Lxybin2.Write()
    eff_GM_pt_Lxybin3.Write()
    eff_DG_pt_Lxybin1.Write()
    eff_DG_pt_Lxybin2.Write()
    eff_DG_pt_Lxybin3.Write()
    eff_GM_pt_dxybin1.Write()
    eff_GM_pt_dxybin2.Write()
    eff_GM_pt_dxybin3.Write()
    eff_DG_pt_dxybin1.Write()
    eff_DG_pt_dxybin2.Write()
    eff_DG_pt_dxybin3.Write()

    total_genMu_eta.Write()
    recoGM_genMu_eta.Write()
    recoDG_genMu_eta.Write()
    eff_GM_eta.Write()
    eff_DG_eta.Write()

    total_genMu_Lxy.Write()
    recoGM_genMu_Lxy.Write()
    recoDG_genMu_Lxy.Write()
    eff_GM_Lxy.Write()
    eff_DG_Lxy.Write()


    outputFile.Close()

