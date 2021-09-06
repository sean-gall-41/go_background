// globals
final int goDim = 19;
float squareSide;
float division;
JSONObject json;
int[][] moves;
int[][][] pixelCoords;
String firstPlayer;
int colorVal;
int moveIndex;
int alpha;
import java.io.*;
import java.lang.*;
import java.util.*;

public String getPythonScriptName() {
  File f = new File(sketchPath());
  FilenameFilter filter = new FilenameFilter() {
    @Override
    public boolean accept(File f, String name) {
      return name.endsWith(".py");
    }
  };
  
  String[] pathnames = f.list(filter);
  // assume not empty for now
  return sketchPath() + "\\" + pathnames[0];
}

ArrayList<String> pythonCommand() {
  ArrayList<String> command = new ArrayList<String>();
  command.add("python");
  command.add(getPythonScriptName());
  return command;
}

ArrayList<String> condaRunCommand(String env) {
  ArrayList<String> command = new ArrayList<String>();
  command.add("conda");
  command.add("run");
  //command.add("--live-stream");
  command.add("-n");
  command.add(env);
  for (String pythonCommandElem : pythonCommand()) {
    command.add(pythonCommandElem);
  }
  return command;
}


//TODO: create function to obtain the script name
//@Test
public void invokeScript(ArrayList<String> list) throws Exception {
  ProcessBuilder processBuilder = new ProcessBuilder(list);
  processBuilder.redirectErrorStream(true);
   
  Process process = processBuilder.start();
   
  //report python process output to stdOut to the console
  BufferedReader stdInput = new BufferedReader(new InputStreamReader(process.getInputStream()));
  String s = null;
  while ((s = stdInput.readLine()) != null) {
    System.out.println(s);
  }
  
  int exitCode = process.waitFor();
  //assertEquals("No errors should be detected", 0, exitCode);
  assert exitCode == 0 : "No errors should be detected";
   
 }



void setup() {
  // environment setup
  fullScreen();
  background(0);
  
  try { 
    // invoke the python script
    //TODO: bug fix on input in python script with conda execution via Java
    invokeScript(condaRunCommand("go-manip")); 
  } catch (Exception e) {
    System.out.println("Exception thrown: " + e);
  }
  // obtain relevant vars from json file(s)
  //TODO: get filename from the data file directly, not hardcode
  String filename = "Jud-1962-1.json";
  json = loadJSONObject(filename);
  moves = intArrayFromJSONArray(json.getJSONArray("MVS"));
  
  //board geometry setup
  squareSide = 0.75 * pixelHeight;
  division = squareSide / 20;
  pixelCoords = calculateGridPoints(squareSide, division, goDim);
  
  // game info/drawing setup
  moveIndex = 0;
  alpha = 0;
  firstPlayer = json.getString("PL");
  colorVal = firstPlayer.equals("b") ? 55 : 155;
}

void draw(){
  
  // main drawing functions
  translate(pixelWidth/2, pixelHeight/2);
  noStroke();
  fill(colorVal, alpha);
  ellipse(pixelCoords[moves[moveIndex][0]][moves[moveIndex][1]][0],
          pixelCoords[moves[moveIndex][0]][moves[moveIndex][1]][1],
          0.7 * division,
          0.7 * division);
  
  // adjust alpha values for each stone drawn.
  // reset alpha and change color value when we
  // move on to the next move
  alpha += 2;
  if (alpha >= 56) {
    colorVal = colorVal == 55 ? 155 : 55;
    alpha = 0;
    moveIndex++;
  }
  
  delay(40);
  
  // exit gently
  if (moveIndex == moves.length) {
    exit(); 
  }
}

// yes there is an inbuilt function for JSONArrays to do this
// however, does not work for nested arrays, so here we are.
int[][] intArrayFromJSONArray(JSONArray jsonMoves) {
  moves = new int[jsonMoves.size()][2];
  for (int i = 0; i < jsonMoves.size(); i++) {
    JSONArray thisMove = jsonMoves.getJSONArray(i);
    moves[i] = thisMove.getIntArray();
  }
  return moves;
}

// using relevant geometric inputs, calculate the pixel location for
// each "point" on the board
int[][][] calculateGridPoints(float squareSide, float division, final int goDim) {
  float halfSquareSide = squareSide / 2;
  int[][][] pixelCoords = new int[goDim][goDim][2];
  translate(pixelWidth/2, pixelHeight/2);
  // obtain pixel values for grid points
  float pX = -halfSquareSide + division;
  for (int i = 0; i < goDim; i++) {
    float pY = -halfSquareSide + division;
    for (int j = 0; j < goDim; j++) {
      pixelCoords[i][j][0] = int(pX);
      pixelCoords[i][j][1] = int(pY);
      pY += division;
    }
    pX += division;
  } 
  return pixelCoords;
}
