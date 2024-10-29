# I N T E R S T E L L A R
## Interstellar Movie Interactions Network

### Overview
This project visualizes the interactions network between characters from the movie *Interstellar*, based on the 2014 final script compared to the 2008 draft version. By analyzing and comparing these versions, we can observe changes in character roles and interactions, while noting that some characters remain consistent.

![Interstellar Network](https://github.com/annguyen-git/interstellar-movie-interactions-analytics/blob/main/resources/interaction_network.gif)

You can explore the interactive networks here:
- [Interstellar movie 2014 script, interactive network](https://annguyen-git.github.io/interstellar-movie-interactions-analytics/output/interstellar_2014.html)
- [Interstellar movie 2008 script, interactive network](https://annguyen-git.github.io/interstellar-movie-interactions-analytics/output/interstellar_2008.html)

### Prerequisites
Make sure to install the required packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```
### Workflow

The following steps outline the process used to generate and visualize the character interaction networks:

1. **Load and Convert Scripts**: 
   - Download the PDF versions of the *Interstellar* scripts (2014 and 2008 versions) from online sources.
   - Convert each PDF script into a text file for easier parsing.

2. **Parse Script Structure**: 
   - Process each script's text to structure character names by sequence in each scene.
   - Identify each character’s appearances and the sequence of their interactions.

3. **Define Interactions**:
   - **Direct Interactions**: Count characters appearing one after another in the script sequence as direct interactions.
   - **Indirect Interactions**: When two characters appear in the same scene with another character mentioned between them, count this as an indirect interaction.

4. **Create Network Graph**:
   - Use the `NetworkX` library to create a graph from the parsed interaction data, where each character is a node.
   - Add edges between nodes based on direct and indirect interactions, assigning weights based on interaction counts.

5. **Visualize with Pyvis**:
   - Import the `NetworkX` graph into `Pyvis` to create an interactive HTML visualization.
   - Customize the node sizes based on each character's total interactions and adjust edge thickness to reflect interaction frequency.
   - Save the visualizations as HTML files in the `output/` directory for easy viewing.

Please see funtions.py and notebook file for more details.
