import adsk.core, adsk.fusion, json

def run(_context: str):
    app = adsk.core.Application.get()
    source = adsk.fusion.Design.cast(app.activeDocument.products.itemByProductType('DesignProductType'))
    assert app.activeDocument.name == 'Modelo referência', 'Selecione o documento de referencia antes de gerar a campanha.'
    tm = adsk.fusion.TemporaryBRepManager.get()
    solid = tm.copy(source.rootComponent.bRepBodies.item(0))
    original_volume = source.rootComponent.bRepBodies.item(0).physicalProperties.volume
    doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
    doc.name = 'Garra - campanha FFF 30 40 60 100'
    design = adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'))
    design.designType = adsk.fusion.DesignTypes.DirectDesignType
    root = design.rootComponent
    original = root.bRepBodies.add(solid)
    original.name = 'Referencia macica 100pct'
    skin = root.bRepBodies.add(tm.copy(solid))
    skin.name = 'Casca 2mm - construcao'
    entities = adsk.core.ObjectCollection.create()
    entities.add(skin)
    shell_input = root.features.shellFeatures.createInput(entities)
    shell_input.insideThickness = adsk.core.ValueInput.createByString('2 mm')
    shell = root.features.shellFeatures.add(shell_input)
    assert shell is not None
    skin = root.bRepBodies.itemByName('Casca 2mm - construcao')
    assert skin is not None
    core = tm.copy(solid)
    assert tm.booleanOperation(core, tm.copy(skin), adsk.fusion.BooleanTypes.DifferenceBooleanType)
    core_body = root.bRepBodies.add(core)
    core_body.name = 'Interior elegivel - construcao'
    record = {'source_document':source.parentDocument.name, 'solid_volume_cm3':original_volume,
              'shell_thickness_mm':2, 'shell_volume_cm3':skin.physicalProperties.volume,
              'core_volume_cm3':core_body.physicalProperties.volume,
              'infill_type':'grade vertical explicita XY, paredes e tampas fechadas', 'pitch_mm':20}
    root.attributes.add('FFF_CAMPAIGN','GeometryDefinition',json.dumps(record))
    original.isLightBulbOn = False
    core_body.isLightBulbOn = False
    app.activeViewport.fit()
    print(json.dumps(record))
