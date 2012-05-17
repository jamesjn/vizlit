import os
import vtk
import time
import os.path

class Figure:

  def generate(self, name, imDim1, imDim2, imDim3, rotation_azimuth, rotation_elevation):

    #THIS METHOD NEEDS SERIOUS REFACTORING

    FILE = open("/home/jchiang/dev/django/vizlit/generator/vtk_scripts/problem1.txt","r");

    #Define readlist to store non-empty lines from the input.txt file

    readlist = [];

    #Read from the file one line at a time and store it in readlist

    for line in FILE:
      readlist.append(line);line


    #for now we will use 

    #imDimensions = readlist[2].split(' ');
    layerLocs = readlist[4].split(' ');
    layerColors = readlist[6].split(' ');
    originSlice = readlist[8].split(' ');
    point1Slice = readlist[10].split(' ');
    point2Slice = readlist[12].split(' ');
    rotationDiagram = readlist[14].split(' ');
    fileOutput = '/home/jchiang/dev/django/vizlit/generator/images/' + name;

    print originSlice;

    xDim = imDim1 #int(imDimensions[0]);
    yDim = imDim2 #int(imDimensions[1]);
    zDim = imDim3 #int(imDimensions[2]);

    ### End File input ###

    #Image Data definition. Variable declarations are not necessary in python.
    #set imData to an instance of vtkImageData
    imData = vtk.vtkImageData();

    #The dimensions
    imData.SetDimensions(xDim,yDim,zDim);

    #We set the scalar type to unsigned short, scalar components to 1 and allocate it
    imData.SetScalarTypeToUnsignedShort();
    imData.SetNumberOfScalarComponents(1);
    imData.AllocateScalars();

    #Scalars array definition and memory allocation
    scalars = vtk.vtkUnsignedShortArray();
    scalars.SetNumberOfValues(xDim*yDim*zDim);


    #The three 'for' loops to enter the scalar values into the image data

    for i in range(0, zDim):
      z = i;
      iOffset = (i*xDim*yDim);
      for j in range(0,yDim):
        y = j;
        jOffset = (j*xDim);
        for k in range(0,xDim):
          x = k;
          offset = (k+iOffset+jOffset);
          for m in range(0, len(layerLocs)-1):
            if y>=int(layerLocs[m]) and y<int(layerLocs[m+1]):
              scalars.InsertTuple1(offset, m+1);



    (imData.GetPointData()).SetScalars(scalars);

    colorTransferFunction = vtk.vtkColorTransferFunction();

    colorTransferFunction.AddRGBPoint(0,1,1,1);

    for i in range(1, len(layerColors)):
      tempColor = layerColors[i-1].split(',');
      colorTransferFunction.AddRGBPoint(float(i),float(tempColor[0]), float(tempColor[1]), float(tempColor[2]));

    opacityTransferFunction = vtk.vtkPiecewiseFunction();
    opacityTransferFunction.AddPoint(0,0);
    opacityTransferFunction.AddPoint(1,1);

    compositeFunction = vtk.vtkVolumeRayCastCompositeFunction();

    volMapper = vtk.vtkVolumeRayCastMapper();
    volMapper.SetInput(imData);
    volMapper.SetVolumeRayCastFunction(compositeFunction);

    volumeProperty = vtk.vtkVolumeProperty();
    volumeProperty.SetColor(colorTransferFunction);
    volumeProperty.SetScalarOpacity(opacityTransferFunction);
    volumeProperty.ShadeOn();
    volumeProperty.SetDiffuse(0.7);
    volumeProperty.SetAmbient(0.8);
    volumeProperty.SetSpecular(0.5);
    volumeProperty.SetSpecularPower(70.0);

    volVolume = vtk.vtkVolume();
    volVolume.SetMapper(volMapper);
    volVolume.SetProperty(volumeProperty);
    light = vtk.vtkLight();

    light.SetColor(1,1,1);
    light.SetPosition(30,500,150);
    light.SetFocalPoint(50,50,50);
    light.SetIntensity(0.9);

    volMapper2 = vtk.vtkVolumeRayCastMapper();
    volMapper2.SetInput(imData);
    volMapper2.SetVolumeRayCastFunction(compositeFunction);

    plane1 = vtk.vtkPlaneSource();
    plane1.SetOrigin(float(originSlice[0]),float(originSlice[1]),float(originSlice[2]));
    plane1.SetPoint1(float(point1Slice[0]),float(point1Slice[1]),float(point1Slice[2]));
    plane1.SetPoint2(float(point2Slice[0]),float(point2Slice[1]),float(point2Slice[2]));

    planeProperty = vtk.vtkProperty();
    #planeProperty.SetColor(1,1,1);

    planeMapper = vtk.vtkPolyDataMapper();
    planeMapper.SetInputConnection(plane1.GetOutputPort());

    planeProperty = vtk.vtkProperty();
    #planeProperty.SetOpacity(1);
    planeProperty.SetLineWidth(5);

    planeActor = vtk.vtkActor();
    planeActor.SetMapper(planeMapper);
    planeActor.SetProperty(planeProperty);
    (planeActor.GetProperty()).SetColor(0,0,0);

    planeNormal = plane1.GetNormal();
    planeCenter = plane1.GetCenter();
    testNormal = [0,0,0];
    testNormal[0] = planeNormal[0]*-1;
    testNormal[1] = planeNormal[1]*-1;
    testNormal[2] = planeNormal[2]*-1;

    clipPlane1 = vtk.vtkPlane();
    clipPlane1.SetOrigin(float(originSlice[0]),float(originSlice[1]),float(originSlice[2]));
    clipPlane1.SetNormal(plane1.GetNormal());
    volMapper2.AddClippingPlane(clipPlane1);

    print testNormal;

    originSlice2 = [0,0,0];
    originSlice2[0] = float(originSlice[0]) - float(testNormal[0])*3;
    originSlice2[1] = float(originSlice[1]) - float(testNormal[1])*3;
    originSlice2[2] = float(originSlice[2]) - float(testNormal[2])*3;


    print originSlice2;

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

    (ren.GetActiveCamera()).Azimuth(float(rotation_azimuth));
    (ren.GetActiveCamera()).Elevation(float(rotation_elevation));
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

