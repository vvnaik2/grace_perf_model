from m5.objects import *
from common.cores.arm.O3_ARM_v7a import *
from common.Caches import *

# Sources for this configuration:
# (1) Neoverse_V2 TRM ( 102375_0001_02_en):
# https://developer.arm.com/documentation/102375/latest/
# (2) Grace CPU Superchip whitepaper

class O3_ARM_Neoverse_V2_ICache_128(Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 8
    tgts_per_mshr = 16
    size = '64kB'# (1)
    assoc = 4# (1)
    writeback_clean = False
    prefetcher = StridePrefetcher(degree=1)

class O3_ARM_Neoverse_V2_DCache_128(Cache):
    tag_latency = 3
    data_latency = 3
    response_latency = 1
    tgts_per_mshr = 16
    writeback_clean = False
    size = '64kB'# (1)
    mshrs = 20
    assoc = 4 # (1)
   #prefetcher = StridePrefetcher(degree=16, latency = 1)

class O3_ARM_Neoverse_V2_L2_128(Cache):
    tag_latency = 5
    data_latency = 5
    response_latency = 2
    mshrs = 46
    tgts_per_mshr = 16
    clusivity = 'mostly_incl'
    assoc = 8# (1)
    size = '2MB'# Grace CPU - 2 MB ( 1 or 2 as per TRM)
    writeback_clean= True

class O3_ARM_Neoverse_V2_L3_128(L3Cache):
    tag_latency = 48
    data_latency = 48
    response_latency = 16
    assoc = 16
    size = '128MB'#(2)#Grace cpu config is 234 (not a power of 2)
    clusivity = 'mostly_excl'
    mshrs = 128



#Seperated each Vec execution units :
#O3_ARM_Neoverse_V2_FP_Vec_0_128 - Contains all the
#gem5 OpClass corresponds to V, V01, V02 and V0 in (1) table 3.1

class O3_ARM_Neoverse_V2_FP_Vec_0_128(FUDesc):
    opList = [
        #FP arith (fadd)-3.12
        OpDesc(opClass='FloatAdd', opLat=2),
        #FP compare (fccmpe)-3.12
        OpDesc(opClass='FloatCmp', opLat=2),
        #Fp (vfma)-3.12
        OpDesc(opClass='FloatMultAcc', opLat=4),
        #Fp convert (vcvt)-3.13
        OpDesc(opClass='FloatCvt', opLat=3),
        #Vec arith basis (add)-3.16
        OpDesc(opClass='SimdAdd', opLat=2),
        #Vec logical (and)  -3.16
        OpDesc(opClass='SimdAlu', opLat=2),
        #Vec compare (cmeq) -3.16
        OpDesc(opClass='SimdCmp', opLat=2),
        #miscelleaneaus
        OpDesc(opClass='FloatMisc', opLat=3),
        # (vadd) -3.17
        OpDesc(opClass='SimdFloatAdd',opLat=2),
        #Vec (vmla)-3.17
        OpDesc(opClass='SimdFloatMultAcc',opLat=4),
        #Vec FP comapre (fcmgt)-3.17
        OpDesc(opClass='SimdFloatCmp', opLat=2),
        #SVE FP Red f64 (fmaxv)
        OpDesc(opClass='SimdFloatReduceCmp', opLat=3),
        #Fp multiply (fmul)-3.12
        OpDesc(opClass='FloatMult', opLat=3),
        #Fp multiply (fmul)-3.22
        OpDesc(opClass='SimdAes', opLat=2),
        #Fp multiply (fmul)-3.22
        OpDesc(opClass='SimdAesMix', opLat=2),
        #Vec integer multiply(mul)-3.16
        OpDesc(opClass='SimdMult',opLat=4),
        #Vec move, immed (vmov) -3.16
        OpDesc(opClass='SimdMisc', opLat=2),
        #SVE reduction (saddv)-3.16
        OpDesc(opClass='SimdReduceAdd', opLat=2),
        #SVE reduction, logical (andv)
        OpDesc(opClass='SimdReduceAlu', opLat=3),
        #SVE FP associative add (fadda)
        OpDesc(opClass='SimdFloatReduceAdd', opLat=2, pipelined=False),
        # misc insts (vneg)-3.17
        OpDesc(opClass='SimdFloatMisc', opLat=2),
        #PREDALU has instructions in V group ( trn1 and uzp )
        OpDesc(opClass='SimdPredAlu', opLat=2),

        #V02 and V01
        #Fp divide (vdiv)- average latency-3.13
        OpDesc(opClass='FloatDiv', opLat=11, pipelined=False),
        #Vec FP divide f64 (fdiv)- we take average latency-3.17
        OpDesc(opClass='SimdFloatDiv', opLat=11, pipelined=False),
        #Fp square root D-form (fsqrt)- average latency-3.13
        OpDesc(opClass='FloatSqrt', opLat=12, pipelined=False),
        #Vec reciprocal estimate (vrsqrte)
        OpDesc(opClass='SimdSqrt', opLat=9),
        #Vec FP square root f64 (vsqrt)- we take average latency-3.17
        OpDesc(opClass='SimdFloatSqrt', opLat=12, pipelined=False),

        #Vec multiply accumulate, D-form (mla) -3.16
        OpDesc(opClass='SimdMultAcc',opLat=4),
        #Vec FP convert to FP 64b (scvtf)-3.17
        OpDesc(opClass='SimdCvt', opLat=3),

        #V0
        #Crypto SHA1 hash acceleration op(sha1h) - 2 latency -3.22
        OpDesc(opClass='SimdSha1Hash2',opLat=2),
        #Crypto SHA1 hash acceleration ops (SHA1M)-3.22
        OpDesc(opClass='SimdSha1Hash',opLat=4),
        #Crypto SHA1 schedule acceleration ops (SHA1SU0)-3.22
        OpDesc(opClass='SimdShaSigma3',opLat=2),
        #Crypto SHA256 hash acceleration ops (SHA256H) -3.22
        OpDesc(opClass='SimdSha256Hash',opLat=4),
        #Crypto SHA256 hash acceleration ops (SHA256H2)-3.22
        OpDesc(opClass='SimdSha256Hash2',opLat=4),
        #Crypto SHA256 schedule acceleration ops(sha256su0)-3.22
        OpDesc(opClass='SimdShaSigma2',opLat=2),
        #Crypto SHA256 schedule acceleration ops(sha256su1)-3.22
        OpDesc(opClass='SimdShaSigma3',opLat=2),

       #store data μOPs
    ]
    count = 1

#O3_ARM_Neoverse_V2_FP_Vec_1_128 - Contains all the gem5 OpClass
# corresponds to V, V01, V13 and V1 in (1) table 3.1
class O3_ARM_Neoverse_V2_FP_Vec_1_128(FUDesc):
    opList = [
        #Common V
        #FP arith (fadd)-3.12
        OpDesc(opClass='FloatAdd', opLat=2),
        #FP compare (fccmpe)-3.12
        OpDesc(opClass='FloatCmp', opLat=2),
        #Fp (vfma)-3.12
        OpDesc(opClass='FloatMultAcc', opLat=4),
        #Fp convert (vcvt)-3.13
        OpDesc(opClass='FloatCvt', opLat=3),
        #Vec arith basis (add)-3.16
        OpDesc(opClass='SimdAdd', opLat=2),
        #Vec logical (and)  -3.16
        OpDesc(opClass='SimdAlu', opLat=2),
        #Vec compare (cmeq) -3.16
        OpDesc(opClass='SimdCmp', opLat=2),
        #miscelleaneaus
        OpDesc(opClass='FloatMisc', opLat=3),
        # (vadd) -3.17
        OpDesc(opClass='SimdFloatAdd',opLat=2),
        #Vec (vmla)-3.17
        OpDesc(opClass='SimdFloatMultAcc',opLat=4),
        #Vec FP comapre (fcmgt)-3.17
        OpDesc(opClass='SimdFloatCmp', opLat=2),
        #SVE FP Red f64 (fmaxv)
        OpDesc(opClass='SimdFloatReduceCmp', opLat=3),
        #Fp multiply (fmul)-3.12
        OpDesc(opClass='FloatMult', opLat=3),
        #Fp multiply (fmul)-3.22
        OpDesc(opClass='SimdAes', opLat=2),
        #Fp multiply (fmul)-3.22
        OpDesc(opClass='SimdAesMix', opLat=2),
        #Vec integer multiply(mul)-3.16
        OpDesc(opClass='SimdMult',opLat=4),
        #Vec move, immed (vmov) -3.16
        OpDesc(opClass='SimdMisc', opLat=2),
        #SVE reduction (saddv)-3.16
        OpDesc(opClass='SimdReduceAdd', opLat=2),
        #SVE reduction, logical (andv)
        OpDesc(opClass='SimdReduceAlu', opLat=3),
        #SVE FP associative add (fadda)
        OpDesc(opClass='SimdFloatReduceAdd', opLat=2, pipelined=False),
        # misc insts (vneg)-3.17
        OpDesc(opClass='SimdFloatMisc', opLat=2),
        #PREDALU has instructions in V group ( trn1 and uzp )
        OpDesc(opClass='SimdPredAlu', opLat=2),

        #V1
        #Vec FP convert to FP 64b (scvtf)-3.17
        OpDesc(opClass='SimdCvt', opLat=3),
        #PREDALU has instructions in V1 group ( COMPACT), EOR
        OpDesc(opClass='SimdPredAlu', opLat=3),

        #V13
        #SVE reduction, arith, S form (smaxv)-3.16
        OpDesc(opClass='SimdReduceCmp', opLat=2),
        #Vec absolute diff accum (vaba) -3.16
        OpDesc(opClass='SimdAddAcc', opLat=4),
        #Vec shift by immed, (shl)-3.16
        OpDesc(opClass='SimdShift',opLat=2),
        #Vec shift accumulate (vsra)-3.16
        OpDesc(opClass='SimdShiftAcc', opLat=4)

    ]
    count = 1

#O3_ARM_Neoverse_V2_FP_Vec_2_128 - Contains all the gem5 OpClass
# corresponds to V and V02 in (1) table 3.1
class O3_ARM_Neoverse_V2_FP_Vec_2_128(FUDesc):
    opList = [
        #FP arith (fadd)-3.12
        OpDesc(opClass='FloatAdd', opLat=2),
        #FP compare (fccmpe)-3.12
        OpDesc(opClass='FloatCmp', opLat=2),
        #Fp (vfma)-3.12
        OpDesc(opClass='FloatMultAcc', opLat=4),
        #Fp convert (vcvt)-3.13
        OpDesc(opClass='FloatCvt', opLat=3),
        #Vec arith basis (add)-3.16
        OpDesc(opClass='SimdAdd', opLat=2),
        #Vec logical (and)  -3.16
        OpDesc(opClass='SimdAlu', opLat=2),
        #Vec compare (cmeq) -3.16
        OpDesc(opClass='SimdCmp', opLat=2),
        #miscelleaneaus
        OpDesc(opClass='FloatMisc', opLat=3),
        # (vadd) -3.17
        OpDesc(opClass='SimdFloatAdd',opLat=2),
        #Vec (vmla)-3.17
        OpDesc(opClass='SimdFloatMultAcc',opLat=4),
        #Vec FP comapre (fcmgt)-3.17
        OpDesc(opClass='SimdFloatCmp', opLat=2),
        #SVE FP Red f64 (fmaxv)
        OpDesc(opClass='SimdFloatReduceCmp', opLat=3),
        #Fp multiply (fmul)-3.12
        OpDesc(opClass='FloatMult', opLat=3),
        #Fp multiply (fmul)-3.22
        OpDesc(opClass='SimdAes', opLat=2),
        #Fp multiply (fmul)-3.22
        OpDesc(opClass='SimdAesMix', opLat=2),
        #Vec integer multiply(mul)-3.16
        OpDesc(opClass='SimdMult',opLat=4),
        #Vec move, immed (vmov) -3.16
        OpDesc(opClass='SimdMisc', opLat=2),
        #SVE reduction (saddv)-3.16
        OpDesc(opClass='SimdReduceAdd', opLat=2),
        #SVE reduction, logical (andv)
        OpDesc(opClass='SimdReduceAlu', opLat=3),
        #SVE FP associative add (fadda)
        OpDesc(opClass='SimdFloatReduceAdd', opLat=2, pipelined=False),
        # misc insts (vneg)-3.17
        OpDesc(opClass='SimdFloatMisc', opLat=2),
        #PREDALU has instructions in V group ( trn1 and uzp )
        OpDesc(opClass='SimdPredAlu', opLat=2),

        #Fp divide (vdiv)- average latency-3.13
        OpDesc(opClass='FloatDiv', opLat=11, pipelined=False),
        #Vec FP divide f64 (fdiv)- we take average latency-3.17
        OpDesc(opClass='SimdFloatDiv', opLat=11, pipelined=False),
        #Fp square root D-form (fsqrt)- average latency-3.13
        OpDesc(opClass='FloatSqrt', opLat=12, pipelined=False),
        #Vec FP convert to FP 64b (scvtf)-3.17
        OpDesc(opClass='SimdCvt', opLat=3),
        #Vec multiply accumulate, D-form (mla) -3.16
        OpDesc(opClass='SimdMultAcc',opLat=4),
        #Vec reciprocal estimate (vrsqrte)
        OpDesc(opClass='SimdSqrt', opLat=9),
        #Vec FP square root f64 (vsqrt)- we take average latency-3.17
        OpDesc(opClass='SimdFloatSqrt', opLat=12, pipelined=False)

    ]
    count = 1

#O3_ARM_Neoverse_V2_FP_Vec_3_128 - Contains all the gem5 OpClass
# corresponds to V and V13 in (1) table 3.1
class O3_ARM_Neoverse_V2_FP_Vec_3_128(FUDesc):
    opList = [
       #Common V
        #FP arith (fadd)-3.12
        OpDesc(opClass='FloatAdd', opLat=2),
        #FP compare (fccmpe)-3.12
        OpDesc(opClass='FloatCmp', opLat=2),
        #Fp (vfma)-3.12
        OpDesc(opClass='FloatMultAcc', opLat=4),
        #Fp convert (vcvt)-3.13
        OpDesc(opClass='FloatCvt', opLat=3),
        #Vec arith basis (add)-3.16
        OpDesc(opClass='SimdAdd', opLat=2),
        #Vec logical (and)  -3.16
        OpDesc(opClass='SimdAlu', opLat=2),
        #Vec compare (cmeq) -3.16
        OpDesc(opClass='SimdCmp', opLat=2),
        #miscelleaneaus
        OpDesc(opClass='FloatMisc', opLat=3),
        # (vadd) -3.17
        OpDesc(opClass='SimdFloatAdd',opLat=2),
        #Vec (vmla)-3.17
        OpDesc(opClass='SimdFloatMultAcc',opLat=4),
        #Vec FP comapre (fcmgt)-3.17
        OpDesc(opClass='SimdFloatCmp', opLat=2),
        #SVE FP Red f64 (fmaxv)
        OpDesc(opClass='SimdFloatReduceCmp', opLat=3),
        #Fp multiply (fmul)-3.12
        OpDesc(opClass='FloatMult', opLat=3),
        #Fp multiply (fmul)-3.22
        OpDesc(opClass='SimdAes', opLat=2),
        #Fp multiply (fmul)-3.22
        OpDesc(opClass='SimdAesMix', opLat=2),
        #Vec integer multiply(mul)-3.16
        OpDesc(opClass='SimdMult',opLat=4),
        #Vec move, immed (vmov) -3.16
        OpDesc(opClass='SimdMisc', opLat=2),
        #SVE reduction (saddv)-3.16
        OpDesc(opClass='SimdReduceAdd', opLat=2),
        #SVE reduction, logical (andv)
        OpDesc(opClass='SimdReduceAlu', opLat=3),
        #SVE FP associative add (fadda)
        OpDesc(opClass='SimdFloatReduceAdd', opLat=2, pipelined=False),
        # misc insts (vneg)-3.17
        OpDesc(opClass='SimdFloatMisc', opLat=2),
        #PREDALU has instructions in V group ( trn1 and uzp )
        OpDesc(opClass='SimdPredAlu', opLat=2),

        #V13
        #SVE reduction, arith, S form (smaxv)-3.16
        OpDesc(opClass='SimdReduceCmp', opLat=2),
        #Vec absolute diff accum (vaba) -3.16
        OpDesc(opClass='SimdAddAcc', opLat=4),
        #Vec shift by immed, (shl)-3.16
        OpDesc(opClass='SimdShift',opLat=2),
        #Vec shift accumulate (vsra)-3.16
        OpDesc(opClass='SimdShiftAcc', opLat=4)
    ]
    count = 1



#This class refers to pipelines Branch0, Integer single Cycles 0,
# Integer single Cycle 1 (symbol B R, and S in 3.2)

class O3_ARM_Neoverse_V2_Simple_Int_128(FUDesc):
    #ALU (Unfortunately branches are put together with IntALU :(
    opList = [ OpDesc(opClass='IntAlu', opLat=1) ]
    count = 6#  V2 : Branch 2 units and Single cycles Integer 4

# This class refers to pipelines integer single/multicycle 1
# (this refers to pipeline symbol F, I, M and M0 in 3.2)
class O3_ARM_Neoverse_V2_Complex_Int_128(FUDesc):
    opList = [
        OpDesc(opClass='IntAlu', opLat=1),#  Int ALU
        OpDesc(opClass='IntMult', opLat=2),#  Int mult
        #Int divide W-form (sdiv)- we take average
        OpDesc(opClass='IntDiv', opLat=5, pipelined=False),
        OpDesc(opClass='IprAccess', opLat=1),#  Prefetch
        #Latency varies alot for different instructions in this group.
        OpDesc(opClass='SimdPredAlu')
    ]
    count = 2# V2 : 2 units of complex int alu

# This class refers to Load/Store0/1
# (symbol L in Neoverse guide table 3-1)
class O3_ARM_Neoverse_V2_LoadStore_128(FUDesc):
    opList = [
        OpDesc(opClass='MemRead'),
        OpDesc(opClass='FloatMemRead'),
        OpDesc(opClass='MemWrite'),
        OpDesc(opClass='FloatMemWrite')
    ]
    count = 2#

class O3_ARM_Neoverse_V2_Load_128(FUDesc):
    opList = [
        OpDesc(opClass='MemRead'),
        OpDesc(opClass='FloatMemRead')
    ]
    count = 1#

class O3_ARM_Neoverse_V2_Store_128(FUDesc):
    opList = [
        OpDesc(opClass='MemWrite'),
        OpDesc(opClass='FloatMemWrite')
    ]
    count = 2#

# class O3_ARM_Neoverse_V2_PredAlu_128(FUDesc):
#     opList = [ OpDesc(opClass='SimdPredAlu')  ]
#     count = 1

class O3_ARM_Neoverse_V2_FUP_128(FUPool):
    FUList = [
        O3_ARM_Neoverse_V2_FP_Vec_0_128(),   #Vec0
        O3_ARM_Neoverse_V2_FP_Vec_1_128(),   #Vec1
        O3_ARM_Neoverse_V2_FP_Vec_2_128(),   #Vec2
        O3_ARM_Neoverse_V2_FP_Vec_3_128(),   #Vec3
        O3_ARM_Neoverse_V2_Simple_Int_128(),   #BR0,1 Integer0,1,2,3
        O3_ARM_Neoverse_V2_Complex_Int_128(),  #Multi int 0,1
        O3_ARM_Neoverse_V2_LoadStore_128(),    #Load/Store 0, 1
        O3_ARM_Neoverse_V2_Load_128(),         #Load 2
        O3_ARM_Neoverse_V2_Store_128()         #Store 0, 1
    ]

# Bi-Mode Branch Predictor
class O3_ARM_Neoverse_V2_BP_128(BiModeBP):
    globalPredictorSize = 8192
    globalCtrBits = 2
    choicePredictorSize = 8192
    choiceCtrBits = 2
    BTBEntries = 4096
    BTBTagSize = 18
    RASSize = 16
    instShiftAmt = 2

class GraceCPU(DerivO3CPU):
    decodeToFetchDelay = 1
    renameToFetchDelay = 1
    iewToFetchDelay = 1
    commitToFetchDelay = 1
    renameToDecodeDelay = 1
    iewToDecodeDelay = 1
    commitToDecodeDelay = 1
    iewToRenameDelay = 1
    commitToRenameDelay = 1
    commitToIEWDelay = 1
    fetchWidth = 8
    fetchBufferSize = 64
    fetchToDecodeDelay = 1
    decodeWidth = 8
    decodeToRenameDelay = 1
    renameWidth = 8
    renameToIEWDelay = 1
    issueToExecuteDelay = 1
    dispatchWidth = 8
    issueWidth = 8
    wbWidth = 8
    iewToCommitDelay = 1
    renameToROBDelay = 1
    commitWidth = 8
    squashWidth = 8
    trapLatency = 13
    backComSize = 5
    forwardComSize = 5

    numROBEntries = 320
    numPhysFloatRegs = 192
    numPhysVecRegs = 192
    numPhysIntRegs = 224

    numIQEntries = 120

    fuPool = O3_ARM_Neoverse_V2_FUP_128()

    switched_out = False
    branchPred = O3_ARM_Neoverse_V2_BP_128()

    LQEntries = 68
    SQEntries = 72
    LSQDepCheckShift = 0
    LFSTSize = 1024
    SSITSize = 1024

