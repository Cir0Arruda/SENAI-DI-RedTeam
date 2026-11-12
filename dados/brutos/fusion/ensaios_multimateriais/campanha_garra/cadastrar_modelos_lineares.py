import adsk.core, adsk.fusion, json
from pathlib import Path

BASE=Path(r'FUSION\ensaios_multimateriais')

def run(_context: str):
    app=adsk.core.Application.get()
    d=adsk.fusion.Design.cast(app.activeProduct)
    manifest=json.loads((BASE/'materiais.json').read_text(encoding='utf-8'))
    tm=app.materialLibraries.itemById('C1EEA57C-3F56-45FC-B8CB-A9EC46A9994C').materials.itemById('PrismMaterial-022')
    nu_values=[0.37,0.38,0.38,0.40,0.39,0.39,0.37,0.39]
    nu_sources=[
        'https://pmc.ncbi.nlm.nih.gov/articles/PMC11901100/ (effective PETG Cubic50, proxy only)',
        'https://repository.lib.ncsu.edu/server/api/core/bitstreams/dcb14eea-b257-4854-a3fa-d8956b276466/content (PCTG different grade)',
        'Assumed from different copolyester PCTG; not a Tritan measurement',
        'https://shura.shu.ac.uk/33603/1/Haid_2024_PhD_TowardsConcussionPrevention.pdf (different printed TPU95A)',
        'https://recipp.ipp.pt/bitstreams/d975a4ec-e230-4160-a03c-17ec170fca87/download (different PA6)',
        'https://pmc.ncbi.nlm.nih.gov/articles/PMC10023978/ (PA12 modeling input)',
        'https://api.lib.kyushu-u.ac.jp/opac_download_md/6787558/eng3267.pdf (different PC)',
        'Assumed PA6 matrix Poisson; not a characterized carbon-fiber composite']
    thermal=[(0.20,1100,70),(0.19,1340,None),(None,None,None),
             (None,None,None),(0.37,1600,97),(0.30,1800,150),(0.25,1300,80),(None,None,None)]
    records=[]
    for index,m in enumerate(manifest['materials']):
        p=m['properties']
        name='FFF '+m['id']+' - EXPLORATORIO LINEAR'
        mat=d.materials.itemByName(name)
        if mat is None:mat=d.materials.addByCopy(tm,name)
        E=p['young_modulus']['value']
        E=E['XY'] if isinstance(E,dict) else E
        nu=nu_values[index]
        U=p.get('ultimate_tensile_strength',{}).get('value',0)
        U=U['XY'] if isinstance(U,dict) else U
        Y=p.get('yield_stress',{}).get('value',0)
        k,cp,alpha=thermal[index]
        # Unknown fields are explicitly zero/unavailable, never inherited from ABS.
        for prop in mat.materialProperties:
            if prop.objectType!='adsk::core::FloatProperty':continue
            key=prop.id
            if key=='structural_Density':prop.value=p['density']['value']*1000
            elif key.startswith('structural_Young_modulus'):prop.value=E*1000
            elif key.startswith('structural_Poisson_ratio'):prop.value=nu
            elif key.startswith('structural_Shear_modulus'):prop.value=E*1000/(2*(1+nu))
            elif key=='structural_Minimum_tensile_strength':prop.value=U*1000
            elif key=='structural_Minimum_yield_stress':prop.value=Y*1000
            elif key.startswith('structural_Thermal_conductivity'):prop.value=k or 0
            elif key.startswith('structural_Thermal_expansion_coefficient'):prop.value=alpha or 0
            elif key=='structural_Specific_heat':prop.value=(cp or 0)/1000
            elif key=='structural_Damping_coefficient':prop.value=0
        rec={'id':m['id'],'name':name,'density_kg_m3':p['density']['value']*1000,
             'E_MPa':E,'nu':nu,'nu_source':nu_sources[index], 'UTS_MPa':U or None,'yield_MPa':Y or None,
             'k_W_mK':k,'cp_J_kgK':cp,'alpha_micro_per_K':alpha,
             'classification':'exploratory_isotropic_linear_mixed_sources_not_calibrated',
             'limitations':['No layer-interface failure model','No temperature/rate dependence','No fatigue/creep/wear model',
                            'Unknown numeric fields are zero in Fusion, not measured zero','TPU only infinitesimal response; no hyperelastic calibration',
                            'XY Young used isotropically; CF directional behavior not represented'],
             'thermal_proxy_sources':['ensaios_multimateriais/cenarios_garra_industrial.json',
                     'https://www.shop.amsler-frey.ch/en?category=24&cmd=generate_datasheet',
                     'https://www.mdpi.com/2313-0105/12/10/413'], 'published_material':m}
        mat.description=json.dumps(rec,ensure_ascii=False)
        mat.materialProperties.itemById('physmat_Comments').value=mat.description
        mat.materialProperties.itemById('structural_source').value='Exploratory FFF mixed sources - see description'
        mat.materialProperties.itemById('structural_ExternalMaterialID').value=''
        mat.materialProperties.itemById('physmat_URL').value=m['source_url']
        app.favoriteMaterials.add(mat)
        d.rootComponent.attributes.add('FFF_SOLVER_MODELS',m['id'],json.dumps(rec,ensure_ascii=False))
        records.append(rec)
    baseline=d.materials.itemByName(records[0]['name'])
    for b in d.rootComponent.bRepBodies:b.material=baseline
    (BASE/'campanha_garra'/'modelos_solver_exploratorios.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Materiais fisicos criados:',len(records))
    print([(b.name,b.material.name,b.physicalProperties.volume) for b in d.rootComponent.bRepBodies])
