# Darwify project's magic number library.

# Space dimensions
WIDTH   = 70
HEIGHT  = 23

# Characters
BACKGROUND  = "·"
BARRIER     = "&"
CORPSE      = "x"
FOOD        = "@"

# Booleans
IS_FOOD_ENABLED = True
IS_MAZE_ENABLED = False

# Numbers & quantities
PI = 3.141592653589793                  #PI
CREATURE_BUFFR_LNGTH = 10_000           #Creature list's lenght
GEN_ENTS  = int(WIDTH * HEIGHT * 0.10)  #Number of generated entities per iteration
FOOD_QTY  = int(WIDTH * HEIGHT * 0.00)  #Food spawned per iteration
POP_BEF_RESET   = int(GEN_ENTS * 0.15)  #Population before reset
MAX_ITERATIONS  = -1                    #Maximum number of iterations
INPT_SGNL_MDFR  = 1                     #Input neurons' signal modifier (coefficient)
NEUT_SGNL_MDFR  = 1                     #Neutral neurons' signal modifier (coefficient)
OUT_SGNL_MDFR   = 1                     #Output neurons' signal modifier (coefficient)
NEUR_NEUT_QTY   = 20                    #Number of neutral neurons in one's neural structure
NTRNT_ON_KILL   = 0.1                   #Nutrition given on kill. Killing will spawne a corpse!
DEFAULT_STRTN   = 1                     #Default saturation (hunger) for each entity
NTRTN_CRPS      = 1.00                  #Nutrition given by eating an entity
NTRTN_FOOD      = 0.3                   #Nutrition given by eating some food
PHE_STGHT   = 4                         #Pheromones released each time
GENE_QTY    = 120                       #Genes per entity
PHE_MULT    = 0.999                     #Constant, growth of pheromone intensity per avg pheromone trail
MAX_TIME    = 20.00                     #Maximum simulation time before break in iteration
MAX_GENE    = 16383                     #Maximum gene, rationally
MIN_GENE    = 0                         #Minimum gene, rationally
HF_OSC_PRID = 0.5                       #Half oscillation period in OSC neuron. 

# Probabilities (Prob values go from 0 to 1)
HUNGER_DTH_PROB = 0.05000 #Scalar that multiplies the raw prob. of death by starvation
NEUR_FIRE_PROB  = 0.30000 #Probability factor of a neuron to fire
RND_SPAWN_PROB  = 0.50000 #Probability of randomly generating a new entity instead of recombining it
GENE_VAR_PROB   = 0.10000 #Probability of a gene's base to be changed in reinitialization
RND_ACT_PROB    = 0.10000 #Scalar that multiplies the raw prob. of firing of the rnd neuron
PICK_PROB       = 0.00001 #Standard probability of an entity to be duplicated (see code)

# Differentials
dSTRTN      = -0.002                    #Istantaneous rate of change in saturation
dTIME       =  0.01                     #Istantaneous rate of change in time

# Counters
EXCEPTION_QTY   = 0     #Number of exceptions found
TOT_GEN_ENTS    = 0     #Total generated entities
ITERATIONS      = 0     #Number of iterations done successfully
TIME            = 0     #Time counter

# Lists & storages
CUSTOM_GENOME = []
CREATURES_ON_SCREEN = []
CREATURES = []