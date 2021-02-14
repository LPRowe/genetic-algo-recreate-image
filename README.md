### Image Reconstruction with Genetic Algorithm

🔧 Repository is currenlty under construction 🔧 <br><br>

A more detailed readme is on its way, for now here are the general details:

Each agent consists of a 1D array of n genes where n is the total number of pixels in the target image. 

The first generation starts off with N agents where each agent contains all random values.<br><br>

Then a fitness function (based on the target image) is used to determine which agents are most fit.  Those that are most fit are allowed to survive and breed the next generation.  <br><br>

Breeding is done by crossover with 2 fit agents, and a fraction of the resulting child's genese are randomly mutated.<br><br>

Repeating this process, the agents of each subsequent generation will more closely match the target image.  