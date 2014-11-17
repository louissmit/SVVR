#!/usr/bin/env python

import vtk
import sys
import time


initial_v = 200
min_v = 500
max_v = 36000

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

v16 = vtk.vtkVolume16Reader()
v16.SetDataDimensions(256,256)
v16.SetFilePrefix("/Users/Imperal/Downloads/MysteryData/slice")
v16.SetImageRange(1, 94)
v16.SetDataSpacing(1, 1, 2)


#Creation of Jaw
contour_skeleton = vtk.vtkContourFilter()
contour_skeleton.SetInputConnection(v16.GetOutputPort())
contour_skeleton.SetValue(0, initial_v)
contour_skeleton.ComputeNormalsOn()
# Turn off blue color from contour -> Set color in Actor
# contour_skeleton.ComputeScalarsOff()

normals_skeleton = vtk.vtkPolyDataNormals()
normals_skeleton.SetInputConnection(contour_skeleton.GetOutputPort())
normals_skeleton.SetFeatureAngle(60.0)


mapper_skeleton = vtk.vtkPolyDataMapper()
mapper_skeleton.SetScalarRange(500,5000)
mapper_skeleton.SetInputConnection(normals_skeleton.GetOutputPort())

skeleton = vtk.vtkActor()
skeleton.SetMapper(mapper_skeleton)

# Turn this on if the computation of scalars is off
# skeleton.GetProperty().SetColor(.7,.7,.7)
# skeleton.GetProperty().SetAmbient(.1)
# skeleton.GetProperty().SetDiffuse(1)
# skeleton.GetProperty().SetSpecular(.1)



#Creation of Skin
contour_skin = vtk.vtkContourFilter()
contour_skin.SetInputConnection(v16.GetOutputPort())
contour_skin.SetValue(0, 500)
contour_skin.ComputeNormalsOn()
# Turn off blue color from contour -> Set color in Actor
contour_skin.ComputeScalarsOff()


mapper_skin = vtk.vtkPolyDataMapper()
# Turn off blue color
# mapper.ScalarVisibilityOff()
mapper_skin.SetInputConnection(contour_skin.GetOutputPort())

skin = vtk.vtkActor()
skin.SetMapper(mapper_skin)
skin.GetProperty().SetColor(.5,.5,.5)
skin.GetProperty().SetOpacity(.2)

outlineData = vtk.vtkOutlineFilter()
outlineData.SetInputConnection(v16.GetOutputPort())
mapOutline = vtk.vtkPolyDataMapper()
mapOutline.SetInputConnection(outlineData.GetOutputPort())
outline = vtk.vtkActor()
outline.SetMapper(mapOutline)
outline.GetProperty().SetColor(0.5, 0.5, 0.5)

aCamera = vtk.vtkCamera()
aCamera.SetViewUp(0, 0, -1)
aCamera.SetPosition(0, 1, 0)
aCamera.SetFocalPoint(0, 0, 0)
aCamera.ComputeViewPlaneNormal()

ren.AddActor(outline)
ren.AddActor(skeleton)
ren.AddActor(skin)
ren.SetActiveCamera(aCamera)
ren.ResetCamera()
aCamera.Dolly(1.5)

# Set a background color for the renderer and set the size of the
# render window (expressed in pixels).
ren.SetBackground(.1, .1, .1)
renWin.SetSize(640, 480)
# Note that when camera movement occurs (as it does in the Dolly()
# method), the clipping planes often need adjusting. Clipping planes
# consist of two planes: near and far along the view direction. The
# near plane clips out objects in front of the plane the far plane
# clips out objects behind the plane. This way only what is drawn
# between the planes is actually rendered.
ren.ResetCameraClippingRange()

# Interact with the data.
iren.Initialize()
renWin.Render()

def vtkSliderCallback2(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    contour_skeleton.SetValue(0, pos)

SliderRepres = vtk.vtkSliderRepresentation2D()

SliderRepres.SetMinimumValue(min_v)
SliderRepres.SetMaximumValue(max_v)


SliderRepres.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint1Coordinate().SetValue(0.1, 0.1)
SliderRepres.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint2Coordinate().SetValue(0.9, 0.1)

SliderRepres.SetSliderLength(0.02)
SliderRepres.SetSliderWidth(0.03)
SliderRepres.SetEndCapLength(0.01)
SliderRepres.SetEndCapWidth(0.01)
SliderRepres.SetTubeWidth(0.005)
SliderRepres.SetLabelFormat("%3.0lf")
SliderRepres.SetTitleHeight(0.02)
SliderRepres.SetLabelHeight(0.02)

SliderWidget = vtk.vtkSliderWidget()
SliderWidget.SetInteractor(iren)
SliderWidget.SetRepresentation(SliderRepres)
SliderWidget.KeyPressActivationOff()
SliderWidget.SetAnimationModeToAnimate()
SliderWidget.SetEnabled(True)
SliderWidget.AddObserver("EndInteractionEvent", vtkSliderCallback2)



SliderRepres.SetValue(initial_v)
renWin.Render()
iren.Start()
