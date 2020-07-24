# globalDisplaced-Analyzer



## Crab3 launching in slc7

Some modifications must be done to launch crab3 jobs when using a slc7 machine.

First, assure that you are working with a CMSSW release and arch compatible with crab3 by checking in here: https://cmssdt.cern.ch/SDT/cgi-bin/ReleasesXML

Declare that jobs will be launched with crab standalone [slc7]:

```
source /cvmfs/cms.cern.ch/crab3/crab_slc7_standalone.sh
```

When working with crab in slc7 the attribute 'instance' in the 'ConfigSection' object will be missed and you will need to declare it by adding this line to the crab config file:
``` 
config.General.instance = 'prod'
```

