from PIL import Image
import os
import sys
import subprocess

TITLE = 'POD'

def circuit_dir(name):
	return '..\\Items\\{}\\Circuits\\{}'.format(TITLE, name)

def circuit_mesh_file(name):
	return os.path.join(circuit_dir(name), '{}.fbx'.format(name))

def circuit_item_file(name):
	return os.path.join(circuit_dir(name), '{}.item.xml'.format(name))

def circuit_meshparams_file(name):
	return os.path.join(circuit_dir(name), '{}.meshparams.xml'.format(name))

def circuit_work_dir(name):
	return 'Items/{}/Circuits/{}'.format(TITLE, name)
	
def circuit_work_mesh_file(name):
	return circuit_work_dir(name) + '/{}.fbx'.format(name)

def circuit_work_item_file(name):
	return circuit_work_dir(name) + '/{}.item.xml'.format(name)

def get_all_images(name):
	return [f for f in os.listdir(circuit_dir(name)) if '.png' in f]

def get_color_materials(name):
	with open(os.path.join(circuit_dir(name), 'color_materials.txt'), 'r') as f:
		return [l.strip() for l in f.read().split('\n')]

def convert_image(path):
	img = Image.open(path)
	basename = os.path.basename(path)
	dirname = os.path.dirname(path)
	spl = basename.split('.')
	new_path = os.path.join(dirname, spl[0]) + '_D.tga'
	print('Converting image: {} -> {}'.format(path, new_path))
	img.save(new_path, 'tga')

def meshparams_file_content(images, color_materials):
	res = '<MeshParams MeshType="Static"><Materials>'
	for img in images:
		res += '<Material Name="{0}" Model="TDSN" PhysicsId="TechGround" BaseTexture="{0}" />'.format(img.replace('.png', ''))
	for cm in color_materials:
		res += '<Material Name="{0}" Model="TDSN" PhysicsId="TechGround" BaseTexture="{1}" />'.format(cm, images[0].replace('.png', ''))
	res += '</Materials></MeshParams>'
	return res

def write_meshparams_file(name, images, color_materials):
	with open(circuit_meshparams_file(name), 'w') as f:
		f.write(meshparams_file_content(images, color_materials))
		print('Created: ' + circuit_meshparams_file(name))

def item_file_content(name):
	return """
	<Item Type="StaticObject">
	    <Phy>
	        <MoveShape Type="mesh" File="Items/{1}/Circuits/{0}/{0}.Shape.gbx"/>
	    </Phy>
	    <Vis>
	        <Mesh File="Items/{1}/Circuits/{0}/{0}.Mesh.gbx"/>
	    </Vis>
	    <Levitation VStep="2" />
	</Item>""".format(name, TITLE)

def write_item_file(name):
	with open(circuit_item_file(name), 'w') as f:
		f.write(item_file_content(name))
		print('Created: ' + circuit_item_file(name))

if __name__ == '__main__':
	circuit_name = sys.argv[1]
	images = get_all_images(circuit_name)
	for img in images:
		convert_image(os.path.join(circuit_dir(circuit_name), img))
	write_meshparams_file(circuit_name, images, get_color_materials(circuit_name))
	write_item_file(circuit_name)
	print('NadeoImporter Mesh')
	print(subprocess.run("NadeoImporter Mesh {}".format(circuit_work_mesh_file(circuit_name))))
	print('NadeoImporter Item')
	print(subprocess.run("NadeoImporter Item {}".format(circuit_work_item_file(circuit_name))))