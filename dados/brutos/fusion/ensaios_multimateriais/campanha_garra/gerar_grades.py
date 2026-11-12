import adsk.core, adsk.fusion, json, math

def run(_context: str):
    app=adsk.core.Application.get()
    d=adsk.fusion.Design.cast(app.activeProduct)
    r=d.rootComponent
    tm=adsk.fusion.TemporaryBRepManager.get()
    original=r.bRepBodies.itemByName('Referencia macica 100pct')
    skin=r.bRepBodies.itemByName('Casca 2mm - construcao')
    core=r.bRepBodies.itemByName('Interior elegivel - construcao')
    assert original and skin and core
    vc=core.physicalProperties.volume
    vs=skin.physicalProperties.volume
    solid_volume=original.physicalProperties.volume
    bb=core.boundingBox
    pitch=2.0
    def box(cx,cy,cz,l,w,h):
        return tm.createBox(adsk.core.OrientedBoundingBox3D.create(
            adsk.core.Point3D.create(cx,cy,cz),adsk.core.Vector3D.create(1,0,0),
            adsk.core.Vector3D.create(0,1,0),l,w,h))
    def lattice(a):
        ribs=[]
        # Grade periodica fixa em coordenadas da peca, nao deslocada entre casos.
        for ix in range(math.floor(bb.minPoint.x/pitch), math.ceil(bb.maxPoint.x/pitch)+1):
            ribs.append(box(ix*pitch,(bb.minPoint.y+bb.maxPoint.y)/2,-2.5,a,30,10))
        for iy in range(math.floor(bb.minPoint.y/pitch), math.ceil(bb.maxPoint.y/pitch)+1):
            ribs.append(box((bb.minPoint.x+bb.maxPoint.x)/2,iy*pitch,-2.5,20,a,10))
        grid=ribs[0]
        for rib in ribs[1:]:
            assert tm.booleanOperation(grid,rib,adsk.fusion.BooleanTypes.UnionBooleanType)
        interior=tm.copy(core)
        assert tm.booleanOperation(interior,grid,adsk.fusion.BooleanTypes.IntersectionBooleanType)
        return interior
    records=[]
    for index,target in enumerate([0.30,0.40,0.60]):
        lo,hi=0.01,pitch
        for iteration in range(14):
            a=(lo+hi)/2
            trial=lattice(a)
            probe=r.bRepBodies.add(trial)
            measured=probe.physicalProperties.volume
            assert probe.deleteMe()
            f=measured/vc
            if abs(f-target)<0.001:
                break
            if f<target:lo=a
            else:hi=a
        result=tm.copy(skin)
        assert tm.booleanOperation(result,trial,adsk.fusion.BooleanTypes.UnionBooleanType)
        transform=adsk.core.Matrix3D.create()
        transform.translation=adsk.core.Vector3D.create(index*30,0,0)
        assert tm.transform(result,transform)
        body=r.bRepBodies.add(result)
        body.name=f'GARRA_F{round(target*100)}_GRADE20_CASCA2'
        body.isLightBulbOn=True
        rec={'body':body.name,'target_core_fraction':target,'actual_core_fraction':f,
             'rib_thickness_mm':a*10,'pitch_mm':pitch*10,'shell_mm':2,
             'solid_volume_cm3':solid_volume,'shell_volume_cm3':vs,'core_volume_cm3':vc,
             'material_volume_cm3':body.physicalProperties.volume,
             'offset_x_mm':index*300,'type':'explicit_vertical_XY_grid_not_slicer_gyroid'}
        body.attributes.add('FFF_CAMPAIGN','Infill',json.dumps(rec))
        records.append(rec)
    result=tm.copy(original)
    transform=adsk.core.Matrix3D.create()
    transform.translation=adsk.core.Vector3D.create(90,0,0)
    assert tm.transform(result,transform)
    body=r.bRepBodies.add(result)
    body.name='GARRA_F100_MACICA'
    rec={'body':body.name,'target_core_fraction':1.0,'actual_core_fraction':1.0,
         'shell_mm':2,'solid_volume_cm3':solid_volume,'shell_volume_cm3':vs,
         'core_volume_cm3':vc,'material_volume_cm3':body.physicalProperties.volume,'offset_x_mm':900}
    body.attributes.add('FFF_CAMPAIGN','Infill',json.dumps(rec))
    records.append(rec)
    assert original.deleteMe()
    assert skin.deleteMe()
    assert core.deleteMe()
    r.attributes.add('FFF_CAMPAIGN','GeometryDefinition',json.dumps({'shell_mm':2,'pitch_mm':20,'solid_volume_cm3':solid_volume,'shell_volume_cm3':vs,'core_volume_cm3':vc}))
    r.attributes.add('FFF_CAMPAIGN','InfillModels',json.dumps(records))
    app.activeViewport.fit()
    print(json.dumps(records))
