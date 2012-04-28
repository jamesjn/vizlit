from django.db import models
 
class Figure(models.Model):

  def generate(name):
    FILE = open("/home/jchiang/dev/django/vizlit/generator/vtk_scripts/problem1.txt","r");

    #Define readlist to store non-empty lines from the input.txt file

    readlist = [];

    #Read from the file one line at a time and store it in readlist

    for line in FILE:
      readlist.append(line);	

    #for now we will use 

    imDimensions = readlist[2].split(' ');
    layerLocs = readlist[4].split(' ');
    layerColors = readlist[6].split(' ');
    originSlice = readlist[8].split(' ');
    point1Slice = readlist[10].split(' ');
    point2Slice = readlist[12].split(' ');
    rotationDiagram = readlist[14].split(' ');
    fileOutput = '/home/jchiang/dev/django/vizlit/generator/images/' + name;

    clipPlane2 = vtk.vtkPlane();
    clipPlane2.SetOrigin(float(originSlice2[0]),float(originSlice2[1]),float(originSlice2[2]));
    clipPlane2.SetNormal(testNormal);
    volMapper2.AddClippingPlane(clipPlane2);

    volVolume2 = vtk.vtkVolume();
    volVolume2.SetMapper(volMapper2);
    volVolume2.SetProperty(volumeProperty);

    ren = vtk.vtkRenderer();
    ren2 = vtk.vtkRenderer();
    ren2.AddProp(volVolume2);
    renWin = vtk.vtkRenderWindow();
    renWin.SetSize(800,800);
    renWin2 = vtk.vtkRenderWindow();

    renWin2.SetSize(800,800);
    ren.SetViewport(0,0,1,1);
    ren2.SetViewport(0,0,1,1);
    renWin.AddRenderer(ren);
    renWin2.AddRenderer(ren2);

    iren = vtk.vtkRenderWindowInteractor();
    iren.SetRenderWindow(renWin);

    iren = vtk.vtkRenderWindowInteractor();
    iren.SetRenderWindow(renWin2);

    (ren.GetActiveCamera()).Azimuth(float(rotationDiagram[0]));
    (ren.GetActiveCamera()).Elevation(float(rotationDiagram[1]));
    (ren.GetActiveCamera()).SetParallelProjection(0);

    ren.SetBackground(1,1,1);
    ren2.SetBackground(1,1,1);

    ren.AddLight(light);
    ren.AddProp(volVolume);
    ren.AddActor(planeActor);
    ren.ResetCamera();


    (ren2.GetActiveCamera()).SetFocalPoint(planeCenter);

    upDirection = [float(point1Slice[0])-float(originSlice[0]),float(point1Slice[1])-float(originSlice[1]), float(point1Slice[2])-float(originSlice[2])];

    (ren2.GetActiveCamera()).SetViewUp(upDirection);

    camPosition = [planeCenter[0]-planeNormal[0]*300, planeCenter[1]-planeNormal[1]*300, planeCenter[2]-planeNormal[2]*300];
    (ren2.GetActiveCamera()).SetPosition(camPosition);

    win2imageFilter = vtk.vtkWindowToImageFilter();
    win2imageFilter.SetInput(renWin);

    writerJPEG = vtk.vtkJPEGWriter();
    writerJPEG.SetQuality(100);
    writerJPEG.SetInput(win2imageFilter.GetOutput());
    writerJPEG.SetFileName(fileOutput+".jpg");
    writerJPEG.Write();


    for i in range(0,370,20):
      time.sleep(.03);
      (ren.GetActiveCamera()).Azimuth(-20);
      renWin.AddRenderer(ren);
      win2imageFilter = vtk.vtkWindowToImageFilter();
      win2imageFilter.SetInput(renWin);
      writerJPEG = vtk.vtkJPEGWriter();
      writerJPEG.SetInput(win2imageFilter.GetOutput());
      writerJPEG.SetFileName(fileOutput+"_rotate_"+str(i)+".jpg");
      writerJPEG.Write();

      
