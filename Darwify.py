# (c) First edit on: 07 September 2023, made entirely by Nonna.
# This code is licensed under MIT license (see LICENSE.txt for details)

from magicNumbers   import *
from vectors        import *

from random         import randint, random, choice
from math           import tanh, cos, sin
from copy           import deepcopy

import mazeGenerator
import utils
import DSP

creatureSpace   = None
pheromoneSpace  = None

def eventOccurs(probability: float) -> bool:                    return (random() < probability)

def printSpace(space: DSP.Space) -> None:
    for      i   in space.matrix[::-1]:
        for  ii  in i:
            if isinstance(ii, Creature):
                symbol = creatureSprites[ii.facingDirection % 4]
                print(f'\033[1m\x1b[34m{symbol}\x1b[0m\033[0m', end=" ")
            elif ii == BACKGROUND: print(f"\033[1m\x1b[30m{BACKGROUND}\033[0m\x1b0", end = " ")
            elif ii ==    BARRIER: print(f"\033[1m\x1b[30m{BARRIER}\033[0m\x1b0",    end = " ")
            elif ii ==     CORPSE: print(f"\x1b[31m{CORPSE}\x1b[0m",                 end = " ")
            elif ii ==       FOOD: print(f"\x1b[36m{FOOD}\x1b[0m",                   end = " ")
            else:                  print(ii, end = " ")
        print("\n", end = "")
    print("\n"    , end = "")

    return None

class Creature:
    def __init__(self, genome: tuple, position: tuple) -> object:
        global TOT_GEN_ENTS
        TOT_GEN_ENTS += 1

        self.position           = position
        self.genome             = genome

        self.facingDirection    = randint(0, 4)
        self.saturation         = 1
        self.kills              = 0

        self.inputs             = [0 for _ in inputs]
        self.neutrals           = [0 for _ in range(NEUR_NEUT_QTY)]

        self.weights            = []

        self.weights.append(list(list(0 for i in range(NEUR_NEUT_QTY)) for j in range(len(inputs)  )))
        self.weights.append(list(list(0 for i in range(len(outputs) )) for j in range(NEUR_NEUT_QTY)))

        for gene in self.genome:
            sourceLayer  = utils.getBit(gene,    13)
            source       = utils.getBit(gene, 8, 12) % len(inputs   if not sourceLayer else self.neutrals)
            sink         = utils.getBit(gene, 3,  7) % len(self.neutrals if not sourceLayer else outputs)
            weight       = utils.getBit(gene, 0,  1) * ((-1) ** utils.getBit(gene, 2))
            self.weights[sourceLayer][source][sink] = weight

        spawnCreature(self, creatureSpace)

def flatten_concatenation(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list

def countCreatures(space: DSP.Space) -> int:
    n = 0

    for i in flatten_concatenation(space.matrix):
        if isinstance(i, Creature):
            n += 1
    return n

def spawnCreature(creature: Creature, space: DSP.Space) -> None:

    DSP.point(space,creature.position, creature)
    return None

def forwardPosition(creature: Creature, distance: int = 1) -> tuple:
    direction = directions[creature.facingDirection % 4]
    
    if distance != 1: direction = scaleVector(distance, direction)

    return vectorialSum(creature.position, direction)

def forwardObject(creature: Creature) -> object:

    return DSP.point(creatureSpace, forwardPosition(creature))

def moveCreature(creature: Creature, direction: int) -> None:
    newPosition  = vectorialSum(directions[direction % 4], creature.position)

    if  DSP.point(creatureSpace, newPosition)  ==   BACKGROUND:

        DSP.point(creatureSpace, creature.position, BACKGROUND)
        creature.position        = newPosition

        DSP.point(creatureSpace, creature.position,   creature)
        creature.facingDirection = direction

    return None

def spinCreature(creature: Creature, rotation: int) -> None:

    creature.facingDirection += rotation
    return None

def creatureAttacks(creature: Creature) -> bool:

    attackee = forwardObject(creature)

    if isinstance(attackee, Creature):
        killCreature(attackee)
        creature.kills      +=   1
        creature.saturation +=   NTRNT_ON_KILL; return  True
    elif attackee == CORPSE:
        DSP.point(creatureSpace, forwardPosition(creature), BACKGROUND)
        creature.saturation +=      NTRTN_CRPS; return  True
    elif attackee ==   FOOD:
        DSP.point(creatureSpace, forwardPosition(creature), BACKGROUND)
        creature.saturation +=      NTRTN_FOOD; return  True
    else:                                       return False

def killCreature(creature: Creature):

    CREATURES_ON_SCREEN.remove(creature)
    DSP.point(creatureSpace, creature.position, CORPSE)

    return None

def populationDensityAt(creature: Creature) -> int:
    n = 0

    for i in range(8):
        position = vectorialSum(creature.position, directions[i])
        n       += isinstance(DSP.point(creatureSpace, position), Creature)
    return n

def  pheromoneDensityAt(creature: Creature) -> int:
    n = 0

    for i in range(9):
        position = vectorialSum(creature.position, directions[i])
        
        if DSP.isWithin(pheromoneSpace, position):
            n += DSP.point(pheromoneSpace, position)
    return n

def leavePheromones(creature: Creature) -> None:

    newValue = DSP.point(pheromoneSpace, creature.position) + PHE_STGHT
    _        = DSP.point(pheromoneSpace, creature.position,   newValue)
    
    return None

def leaveFood(creature: Creature) -> bool:
    if not IS_FOOD_ENABLED:  return False

    if creature.saturation > 0 and forwardObject(creature) == BACKGROUND:
        DSP.point(creatureSpace,   forwardPosition(creature),      FOOD)
        creature.saturation -= NTRTN_FOOD
    
    return True

def compareCreatures(self: Creature, other: Creature):

    if not isinstance( self, Creature): return 0
    if not isinstance(other, Creature): return 0

    self   = utils.flatten( self.weights)
    other  = utils.flatten(other.weights)

    cosine = dotProduct(self, other) / (module(self) * module(other))

    return min(max(0, PI/2 - utils.arccos(cosine)), 1)

def execute(creature: Creature, registry: dict, neuronTag: str) -> object:

    return registry[neuronTag](creature)

inputs  = {
    "LOC_X"        : lambda self:                          2 * self.position[0] /  WIDTH - 1,
    "LOC_Y"        : lambda self:                          2 * self.position[1] / HEIGHT - 1,

    "POP_DENS"     : lambda self:                                  populationDensityAt(self),
    "PHE_DENS"     : lambda self:                                   pheromoneDensityAt(self),

    "FACING_SMTH"  : lambda self:                    bool(forwardObject(self) != BACKGROUND),
    "FACING_SIMIL" : lambda self:                compareCreatures(self, forwardObject(self)),

    "HUNGER"       : lambda self:                                1 - min(self.saturation, 1),
    "AGE"          : lambda self:                                           min(TIME / 5, 1),

    "RND1"         : lambda self:                          (random() * 2 - 1) * RND_ACT_PROB,
    "RND2"         : lambda self:                          (random() * 2 - 1) * RND_ACT_PROB,
    "SIN"          : lambda self:                               sin(PI * TIME / HF_OSC_PRID),
    "COS"          : lambda self:                               cos(PI * TIME / HF_OSC_PRID),
    "TRUE"         : lambda self:                                                        0.5}

outputs = {
    "MOVE_NORTH"   : lambda self:                                      moveCreature(self, 0),
    "MOVE_EAST"    : lambda self:                                      moveCreature(self, 1),
    "MOVE_SOUTH"   : lambda self:                                      moveCreature(self, 2),
    "MOVE_WEST"    : lambda self:                                      moveCreature(self, 3),

    "MOVE_FWD"     : lambda self:               moveCreature(self, self.facingDirection    ),
    "MOVE_LEFT"    : lambda self:               moveCreature(self, self.facingDirection - 1),
    "MOVE_RIGHT"   : lambda self:               moveCreature(self, self.facingDirection + 1),
    "MOVE_BACK"    : lambda self:               moveCreature(self, self.facingDirection + 2),

    "MOVE_RND"     : lambda self:                          moveCreature(self, randint(0, 3)),

    "LEAVE_PHE"    : lambda self:                                      leavePheromones(self),
    "LEAVE_FOOD"   : lambda self:                                      leaveFood(self)      ,

    "SPIN_CLW"     : lambda self:                                     spinCreature(self,  1),
    "SPIN_CNTCLW"  : lambda self:                                     spinCreature(self, -1),

    "KILL_FWD"     : lambda self:                                      creatureAttacks(self),
    "SUICIDE"      : lambda self:                                         killCreature(self)}

def creatureUpdate(creature: Creature) -> None:
    creature.saturation += dSTRTN

    if creature.saturation < 0 and random() < -creature.saturation * HUNGER_DTH_PROB:

        return killCreature(creature)

    for i, neuron in enumerate(inputs):

        creature.inputs[i] = execute(creature, inputs, neuron)

    for i, neuron in enumerate(creature.neutrals):

        sigma = sum(input_value  *  creature.weights[0][j][i] for j,  input_value  in enumerate  (creature.inputs))
        creature.neutrals[i] = tanh(sigma * NEUT_SGNL_MDFR)

    for i, neuron in enumerate(outputs):

        sigma = sum(neutral_value * creature.weights[1][j][i] for j, neutral_value in enumerate(creature.neutrals))
        if eventOccurs(tanh(sigma * OUT_SGNL_MDFR)): execute(creature, outputs, neuron)

    return None
 
def makeGenome(genomeLenght: int = GENE_QTY) -> tuple[int]:

    return list(randint(MIN_GENE, MAX_GENE) for i in range(genomeLenght))

def makeSpawnPoint() -> tuple[int]:

    i = randint(0,  WIDTH - 1)
    j = randint(0, HEIGHT - 1)

    while DSP.point(creatureSpace, (i, j)) != BACKGROUND:
        i = randint(0,  WIDTH - 1)
        j = randint(0, HEIGHT - 1)

    return (i, j)

def generateFood(space: DSP.Space) -> bool:

    for i in range(FOOD_QTY):
        DSP.point(space, makeSpawnPoint(), FOOD)

    return FOOD_QTY != 0

def mutateCreature(creature: Creature, newPosition: bool = True, geneVarProb = GENE_VAR_PROB) -> Creature:

    genome = [*deepcopy(creature.genome)]
    for i, _ in enumerate(genome):
        genome[i] += (random() < geneVarProb) * randint(0, 1) * (2 ** randint(0, 19))

    position = creature.position
    if newPosition: position = makeSpawnPoint()

    creature = Creature(genome, position)

    return creature

def reducePheromones(space: DSP.Space, barrierSpace: DSP.Space) -> None:    

    newSpace = DSP.Space((WIDTH, HEIGHT), 0)

    for      i  in range(WIDTH ):
        for  j  in range(HEIGHT):

            if DSP.point(barrierSpace, (i, j)) != BACKGROUND: pass
            pheromoneStrenght = 0

            for k in range(9):
                position = vectorialSum((i, j), directions[k])

                if DSP.isWithin(newSpace, position):
                    pheromoneStrenght += DSP.point(space, position) / 9
            DSP.point(newSpace, (i, j), pheromoneStrenght * PHE_MULT)

    return newSpace

def generateMaze(space: DSP.Space) -> None:

    maze = mazeGenerator.generate(space.dimensions[0], space.dimensions[1])

    for i in range(space.dimensions[0]):
        for j in range(space.dimensions[1]):

            if maze[j][i] == mazeGenerator.BARRIER:
                DSP.point(space, (i, j), BARRIER)

    return None

def doIteration():
    global TIME, CREATURES, CREATURES_ON_SCREEN, TOT_GEN_ENTS, ITERATIONS
    global creatureSpace, pheromoneSpace

    creatureSpace  = DSP.Space(  (WIDTH, HEIGHT)  , BACKGROUND)
    pheromoneSpace = DSP.Space(  (WIDTH, HEIGHT)  ,     0     )

    if IS_FOOD_ENABLED: generateFood            (creatureSpace)
    if IS_MAZE_ENABLED: generateMaze            (creatureSpace)

    for i in range(GEN_ENTS):

        print(f"\033[1mGenerating creature, {len(CREATURES_ON_SCREEN)} of {GEN_ENTS}. (\033[0m{('Ooo', 'oOo', 'ooO', 'ooo')[i % 4]})\r", end = "")

        if eventOccurs(RND_SPAWN_PROB) or ITERATIONS == 0:

            creature = Creature(makeGenome() if not bool(CUSTOM_GENOME) else CUSTOM_GENOME, makeSpawnPoint())
            #creature = Creature(makeGenome(), makeSpawnPoint())
            CREATURES                         .append(creature)
            CREATURES_ON_SCREEN               .append(creature)

        else:
            while True:
                for  creature  in  CREATURES :
                    if eventOccurs(PICK_PROB):
                        creature = mutateCreature(creature)

                        CREATURES_ON_SCREEN       .append(creature)
                        CREATURES                 .append(creature)

                        break
                else:   continue
                break

    while TIME < MAX_TIME or MAX_TIME == -1:
        reducePheromones(pheromoneSpace, barrierSpace = creatureSpace)

        print(f"\x1b[34m\033[1mCreature amount\033[0m: {len(CREATURES_ON_SCREEN)} of {GEN_ENTS}    \x1b[34m\033[1mIteration\033[0m: {ITERATIONS}    \x1b[34m\033[1mTime\033[0m: {TIME}\n")
        printSpace(creatureSpace)

        TIME = round(TIME + dTIME, 2)

        for i in CREATURES_ON_SCREEN:
            creatureUpdate(i)
            if len(CREATURES_ON_SCREEN) <= POP_BEF_RESET: break
        else:                                             continue
        break

    CREATURES = sorted(CREATURES, key = lambda self: self.kills, reverse = True)
    CREATURES =        CREATURES[: CREATURE_BUFFR_LNGTH]

    CREATURES_ON_SCREEN         = []
    TIME                        = 0

    ITERATIONS                 += 1

def main():
    global ITERATIONS, EXCEPTION_QTY, TOT_GEN_ENTS
    while  ITERATIONS < MAX_ITERATIONS or MAX_ITERATIONS == -1:
        doIteration()
        try                         :   doIteration()
        except KeyboardInterrupt    :   break
        except                      :   EXCEPTION_QTY += 1

if __name__ == "__main__":
    import resource
    import datetime

    startTime  =  datetime.datetime.now()
    main()
    endTime    =  datetime.datetime.now()

    maxRam = '{:.6f}'.format(abs(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000000 - 0.010368))
    executionTime = endTime - startTime

    logOutput = f"""\n\033[0m\
╔══ \033[1m\x1b[33mE x e c u t i o n   c o m p l e t e d\033[0m ══╗
║                                           ║
║  \033[1m\x1b[33m> Time\033[0m                                   ║
║  \033[1mStarted at\033[0m..{str(startTime).replace("-", "/")[:-3].rjust(27, ".")}  ║
║  \033[1mEnded at\033[0m{str(endTime).replace("-", "/")[:-3].rjust(31, ".")}  ║
║  \033[1mExecution time\033[0m..{str(executionTime)[:-3].rjust(23, ".")}  ║
║  \033[1mTime for iteration (s)\033[0m...{str(round(executionTime.total_seconds()/(ITERATIONS + 0.00001), 7) if ITERATIONS else "........(None)").rjust(14, ".")}  ║
║                                           ║
║  \033[1m\x1b[33m> Performances\033[0m                           ║
║  \033[1mMax ram used\033[0m (gb)..{str(maxRam).rjust(20, ".")}  ║
║                                           ║
║  \033[1m\x1b[33m> Simulation info\033[0m                        ║
║  \033[1mSuccessful iterations\033[0m..{str(ITERATIONS).rjust(16, ".")}  ║
║  \033[1mNumber of exceptions\033[0m..{str(EXCEPTION_QTY).rjust(17, ".")}  ║
║  \033[1mEntities generated\033[0m..{str(TOT_GEN_ENTS).rjust(19, ".")}  ║
║                                           ║
╚═══════════════════════════════════════════╝
"""
    print("\033[1m\x1b[30mList of genomes:", list(i.genome for i in CREATURES_ON_SCREEN))
    print(logOutput)