# Auto generated configuration file
# using: 
# Revision: 1.372.2.1 
# Source: /local/reps/CMSSW.admin/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: GEN-fragment --step GEN,FASTSIM,HLT --beamspot Realistic8TeVCollision --conditions START52_V5::All --pileup 2012_Startup_inTimeOnly --geometry DB--datamix NODATAMIXER --eventcontent AODSIM --datatier AODSIM --no_exec
import FWCore.ParameterSet.Config as cms
from Configuration.Generator.PythiaUESettings_cfi import *

process = cms.Process('HLT')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('FastSimulation.PileUpProducer.PileUpSimulator_2012_Startup_inTimeOnly_cff')
process.load('FastSimulation.Configuration.Geometries_START_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('FastSimulation.Configuration.HLT_GRun_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source(
        "LHESource",

        fileNames = cms.untracked.vstring(),
        )
process.source.fileNames.extend([
'/store/user/ExampleLHE.lhe',
])

process.options = cms.untracked.PSet(
	wantSummary = cms.untracked.bool(False)
)

process.generator = cms.EDFilter("Pythia6HadronizerFilter",
   pythiaHepMCVerbosity = cms.untracked.bool(False),
   maxEventsToPrint = cms.untracked.int32(1),
   pythiaPylistVerbosity = cms.untracked.int32(0),
   comEnergy = cms.double(8000.0),
   PythiaParameters = cms.PSet(
       pythiaUESettingsBlock,
       processParameters = cms.vstring('MSEL=0         ! User defined processes',
                       'PMAS(5,1)=4.4   ! b quark mass',
                       'PMAS(6,1)=172.5 ! t quark mass',
                       'MSTJ(1)=1       ! Fragmentation/hadronization on or off',
                       'PARP(67)=100.0',
                       'MSTP(61)=1      ! Parton showering on or off'),
       parameterSets = cms.vstring('pythiaUESettings',
           'processParameters')
   )
)

process.options.SkipEvent = cms.untracked.vstring('ProductNotFound')

process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    annotation = cms.untracked.string('GEN-fragment nevts:1'),
    name = cms.untracked.string('PyReleaseValidation')
)


process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.AODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('GEN-fragment_GEN_FASTSIM_HLT_PU.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('AODSIM')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)


process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)
process.Realistic8TeVCollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
process.GlobalTag.globaltag = 'START52_V5::All'

process.generation_step = cms.Path(process.generator)
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.AODSIMoutput_step])

