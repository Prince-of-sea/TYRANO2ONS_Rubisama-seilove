from PIL import Image, ImageEnhance
import subprocess
import chardet
import shutil
import glob
import sys
import os
import re



same_hierarchy = (os.path.dirname(sys.argv[0]))#同一階層のパスを変数へ代入
DEFAULT_TXT = os.path.join(same_hierarchy, 'default.txt')


PSP = bool( os.path.isfile(os.path.join(same_hierarchy,'ONS.INI')) )

scenario_dir = os.path.join(same_hierarchy,'data','scenario')
bgimage_dir = os.path.join(same_hierarchy,'data','bgimage')
fgimage_dir = os.path.join(same_hierarchy,'data','fgimage')
bgm_dir = os.path.join(same_hierarchy,'data','bgm')
image_dir = os.path.join(same_hierarchy,'data','image')
others_dir = os.path.join(same_hierarchy,'data','others')
sound_dir = os.path.join(same_hierarchy,'data','sound')

effect_startnum=10
effect_list=[]

str2var_dict={}
str2var_num=[20, 20, 1000]#名前sp,

sel_dict={}


#--------------------def--------------------

def krcmd2krdict(c):
	kr_dict = {}

	for p in re.findall(r'([A-z0-9-_]+?)=("(.*?)"|([^\t\s]+))', c):
		kr_dict[p[0]] = p[2] if p[2] else p[3]

	return kr_dict


def effect_edit(t,f):
	global effect_list

	list_num=0
	if re.fullmatch(r'[0-9]+',t):#timeが数字のみ＝本処理

		for i, e in enumerate(effect_list,effect_startnum+1):#1からだと番号が競合する可能性あり
			if (e[0] == t) and (e[1] == f):
				list_num = i

		if not list_num:
			effect_list.append([t,f])
			list_num = len(effect_list)+effect_startnum

	return str(list_num)


def str2var(s,i):
	global str2var_dict
	global str2var_num

	d=str2var_dict.get(s)

	if d:
		s2=d
	else:
		str2var_dict[s]=str2var_num[i]
		s2=str2var_num[i]
		str2var_num[i]+=1
	
	return s2


def tati_create(storage, width, height, left, top):
	name = ('taticnv/' + storage + '_' + width + '_' + height + '_' + left + '_' + top + '.png')
	namepath = os.path.join(same_hierarchy,name)
	if not os.path.exists(namepath):
		os.makedirs(os.path.dirname(namepath), exist_ok=True)#フォルダなかったら作る

		im = Image.open(os.path.join(fgimage_dir,storage))
		im_r = im.resize((int(width), int(height)))

		im_new = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
		im_new.paste(im_r, (int(640-(int(width)/2)+int(left)), int(top)))
		if PSP:
			im_new = im_new.resize((480, 272))
		im_new.save(namepath)

	return name


def music_cnv():
	pathlist = (glob.glob(os.path.join(sound_dir, '*.*')))
	pathlist += (glob.glob(os.path.join(sound_dir, 'noname_1', '*.*')))
	pathlist += (glob.glob(os.path.join(sound_dir, 'seira_1', '*.*')))
	pathlist += (glob.glob(os.path.join(sound_dir, 'seira_2', '*.*')))

	for f in pathlist:
		fogg = (f + ".ogg")
		try:
			subprocess.run(['ffmpeg', '-y', '-vn',
				'-i', f,
				'-ab', '56k',
				'-ar', '44100',
				'-ac', '2',	fogg,
			], shell=True)
		except:
			pass
		else:
			os.remove(f)
			os.rename(fogg, f)


def bgm_cnv():#一旦wavにしないと動かないのど う し て
	pathlist = (glob.glob(os.path.join(bgm_dir, '*.*')))

	for f in pathlist:
		fn = os.path.basename(f).lower()
		fwav = os.path.join(same_hierarchy, 'data', 'bgm_', str(str2var(fn, 2)) + ".wav")
		fogg = os.path.join(same_hierarchy, 'data', 'bgm_', str(str2var(fn, 2)) + ".ogg")
		os.makedirs(os.path.dirname(fwav), exist_ok=True)#フォルダなかったら作る
		try:
			subprocess.run(['ffmpeg', '-y',
				'-i', f,
				fwav,
			], shell=True)
		except:
			pass

		try:
			subprocess.run(['ffmpeg', '-y',
				'-i', fwav,
				'-ab', '112k',
				'-ar', '44100',
				'-ac', '2',	
				fogg,
			], shell=True)
		except:
			pass
		os.remove(fwav)


#--------------------0.txt作成--------------------
def text_cnv():
	tati_now = {}

	with open(DEFAULT_TXT) as f:
		txt = f.read()

	pathlist = glob.glob(os.path.join(scenario_dir, 'scene_all_v110.ks'))#listにする意味(めんどくさくてコピペしてきた)

	for snr_path in pathlist:
		
		with open(snr_path, 'rb') as f:
			char_code = chardet.detect(f.read())['encoding']

		with open(snr_path, encoding=char_code, errors='ignore') as f:
			#memo
			txt += '\n;--------------- '+ os.path.splitext(os.path.basename(snr_path))[0] +' ---------------\nend\n\n'
			txt = txt.replace('//', ';;;')

			for line in f:
				#最初にやっとくこと
				name_line = re.search(r'#(.*?)\n', line)
				mes_lr_line = re.search(r'(.*?)\[l\]\[r\]\n', line)
				mes_p_line = re.search(r'(.*?)\[p\]\n', line)
				kakko_line = re.search(r'\[(.+?)\]\n', line)

				if re.match('\n', line):#改行は無視
					pass

				elif re.match(r';', line):#元々コメントアウトのやつ目立たせる
					line = r';;;;' + line

				elif name_line:#名前
					line = r'mov $11,"' + name_line[1] + '"\n'

				elif mes_lr_line:#文章＠
					line = mes_lr_line[1].replace(r'?',r'？').replace(r'!',r'！').replace(r'⁉',r'！？').replace(r',',r'') + '@\n'

				elif mes_p_line:#文章￥
					line = mes_p_line[1].replace(r'?',r'？').replace(r'!',r'！').replace(r'⁉',r'！？').replace(r',',r'') + '\\\n'

				elif kakko_line:#[]内
					d = krcmd2krdict('kr_cmd=' + kakko_line[1])
					kr_cmd = d['kr_cmd']

					if kr_cmd == 'bg':
						d_method_ = d.get('method') if d.get('method') else 'crossfade'
						d_time_ = d.get('time') if d.get('time') else '500'
						if d['storage']=='真っ黒.png':
							line = 'vsp 10,0:bg black,' + effect_edit(d_time_, d_method_) + '\n'
						else:
							line = 'vsp 10,0:bg "data\\bgimage_\\' + d['storage'] + '",' + effect_edit(d_time_, d_method_) + '\n'

					elif kr_cmd == 'cg':
						line = 'vsp 10,0:bg "data\\bgimage_\\' + d['storage'] + '",' + effect_edit('500', 'crossfade') + '\n'

					elif kr_cmd == 'chara_new':
						
						if not tati_now.get(d['name']):
							tati_now[d['name']] = {}

						tati_now[d['name']]['storage'] = d['storage']
						tati_now[d['name']]['width'] = d['width']
						tati_now[d['name']]['height'] = d['height']
						tati_now[d['name']]['left'] = d['left']
						tati_now[d['name']]['top'] = d['top']
						
						line = 'lsph ' + str(str2var(d['name'], 1)) + ',"' + tati_create(d['storage'], d['width'], d['height'], d['left'], d['top']) + '",0,0\n'

					elif kr_cmd == 'chara_move':
						d2 = {}
						for a in ['storage', 'width', 'height', 'left', 'top']:
							if d.get(a):					
								tati_now[d['name']][a] = d[a]
								d2[a] = d[a]
							else:
								d2[a] = tati_now[d['name']][a]

						line = 'lsph ' + str(str2var(d['name'], 1)) + ',"' + tati_create(d2['storage'], d2['width'], d2['height'], d2['left'], d2['top']) + '",0,0\n'

					elif kr_cmd == 'chara_show':
						d2 = {}
						for a in ['storage', 'width', 'height', 'left', 'top']:
							if d.get(a):					
								tati_now[d['name']][a] = d[a]
								d2[a] = d[a]
							else:
								d2[a] = tati_now[d['name']][a]
						
						time = d.get('time') if d.get('time') else False
						if time:
							line = 'lsp ' + str(str2var(d['name'], 1)) + ',"' + tati_create(d2['storage'], d2['width'], d2['height'], d2['left'], d2['top']) + '",0,0:print ' + effect_edit(time, 'crossfade') + '\n'
						else:
							line = 'lsph ' + str(str2var(d['name'], 1)) + ',"' + tati_create(d2['storage'], d2['width'], d2['height'], d2['left'], d2['top']) + '",0,0:print 1\n'

					elif kr_cmd == 'chara_mod':
						d2 = {}
						for a in ['storage', 'width', 'height', 'left', 'top']:
							if d.get(a):					
								tati_now[d['name']][a] = d[a]
								d2[a] = d[a]
							else:
								d2[a] = tati_now[d['name']][a]
						
						time = d.get('time') if d.get('time') else False
						if time:
							line = 'lsp ' + str(str2var(d['name'], 1)) + ',"' + tati_create(d2['storage'], d2['width'], d2['height'], d2['left'], d2['top']) + '",0,0:print ' + effect_edit(time, 'crossfade') + '\n'
						else:
							line = 'lsph ' + str(str2var(d['name'], 1)) + ',"' + tati_create(d2['storage'], d2['width'], d2['height'], d2['left'], d2['top']) + '",0,0:print 1\n'

					elif kr_cmd == 'chara_hide':
						time = d.get('time') if d.get('time') else '10'
						line = 'vsp ' + str(str2var(d['name'], 1)) + ',0' + effect_edit(time, 'crossfade') + '\n'

					elif kr_cmd == 'playse':
						line = 'dwave 0,"data/sound/' + d['storage'] + '"\n'

					elif kr_cmd == 'playbgm':
						line = 'bgm "data/bgm_/' + str(str2var(str(d['storage']).lower(), 2)) + '.ogg"\n'

					elif kr_cmd == 'stopbgm':
						line = 'stop\n'

					elif kr_cmd == 'fadeoutbgm':
						line = 'stopfadeout\n'

					elif kr_cmd == 'stopse':
						line = 'dwavestop\n'


					else:
						line = r';' + line#エラー防止の為コメントアウト
						#print(d)


				else:#どれにも当てはまらない、よく分からない場合
					line = r';' + line#エラー防止の為コメントアウト
					#print(line[:-1])


				txt += line

	add0txt_effect = ''
	for i,e in enumerate(effect_list,effect_startnum+1):#エフェクト定義用の配列を命令文に&置換
		add0txt_effect +='effect '+str(i)+',10,'+e[0]+'\n'

	txt = txt.replace(r';<<-EFFECT->>', add0txt_effect)

	fusa = str(str2var('ふさわしきメイドであるために（タイトル画面Ver.）.mp3'.lower(), 2))
	txt = txt.replace(r';<<-TITLE_BGM->>', r'mov $66,"'+fusa+r'.ogg"')

	txt = txt.replace(r';*gameend', r'mov %334,1:reset')
	txt = txt.replace(r'ゲーム本編', '\n*scr_start\n')

	#ガバガバ修正
	txt = txt.replace(r'lsp 20,"taticnv/chara/seira/裸_腕広げ_すまし.png_1416_2000_0_-10.png",0,0:print 14', '')
	txt = txt.replace(r'lsph 23,"taticnv/chara/seira/mainvisual.jpg_1280_1810_0_-400.png",0,0', r'lsp 23,"taticnv/chara/seira/mainvisual.jpg_1280_1810_0_-400.png",0,0:print 15')

	if PSP:
		txt = txt.replace(r';$V2000G200S1280,720L10000', r';$V2000G200S480,272L10000')
		txt = txt.replace(r';<<-PSP_MODE->>', r'mov %199,1')
	else:
		txt = txt.replace(r';<<-PSP_MODE->>', r'mov %199,0')

	open(os.path.join(same_hierarchy,'0.txt'), 'w', errors='ignore').write(txt)


	#画像加工(別にdef取れよって感じだけど)
	for img_path in glob.glob(os.path.join(bgimage_dir, '*.*')):
		os.makedirs(os.path.dirname(img_path.replace('bgimage', 'bgimage_')), exist_ok=True)#フォルダなかったら作る
		if not os.path.basename(img_path).lower()=='logo.png':
			img = Image.open(img_path)
			width, height = img.size

			width_r = 1280 if (not PSP) else 480
			height_r = height*width_r/width

			if PSP:
				if int(height_r) == 270:
					height_r = 272

			img_resize = img.resize((int(width_r), int(height_r)), Image.Resampling.LANCZOS)
			img_resize.save(img_path.replace('bgimage', 'bgimage_'), quality=95)
		else:
			if PSP:
				img = Image.open(img_path)
				width, height = img.size

				width_r = width*480/1280
				height_r = height*480/1280
				
				img_resize = img.resize((int(width_r), int(height_r)), Image.Resampling.LANCZOS)
				img_resize.save(img_path.replace('bgimage', 'bgimage_'), quality=95)

			else:
				shutil.copyfile(img_path, img_path.replace('bgimage', 'bgimage_'))


	#PSP画像加工(別にdef取れよって感じだけど)
	if PSP:
		#正直再帰的に全取得かければよかったと後悔
		#pathlist2 = glob.glob(os.path.join(bgimage_dir, '*.png'))
		#pathlist2.extend(glob.glob(os.path.join(bgimage_dir, '*.jpg')))
		#pathlist2.extend(glob.glob(os.path.join(fgimage_dir, 'chara', 'seira', '*.png')))
		#pathlist2.extend(glob.glob(os.path.join(fgimage_dir, 'chara', 'seira', '*.jpg')))
		pathlist2 = (glob.glob(os.path.join(others_dir, 'plugin', 'seira', 'images', 'background', '*.png')))
		pathlist2.extend(glob.glob(os.path.join(others_dir, 'plugin', 'seira', 'images', 'button', '*.png')))
		pathlist2.extend(glob.glob(os.path.join(others_dir, 'plugin', 'seira', 'images', 'frame', '*.png')))
		pathlist2.extend(glob.glob(os.path.join(others_dir, 'plugin', 'seira', 'images', 'logo', '*.png')))
		pathlist2.extend(glob.glob(os.path.join(image_dir, '*.png')))
		pathlist2.extend(glob.glob(os.path.join(image_dir, 'button', '*.png')))
		pathlist2.extend(glob.glob(os.path.join(image_dir, 'config', '*.png')))
		pathlist2.extend(glob.glob(os.path.join(image_dir, 'title', '*.png')))

		pathlist2.extend(glob.glob(os.path.join(bgimage_dir, 'logo.png')))

		for img_path in pathlist2:
			img = Image.open(img_path)

			width, height = img.size
			width_r = width*480/1280
			height_r = height*480/1280

			if int(height_r) == 270:
				height_r = 272

			img_resize = img.resize((int(width_r), int(height_r)))

			if os.path.basename(img_path).lower()=='frame.png':#フレーム明るすぎて文字見えないので暗くする
				enhancer = ImageEnhance.Brightness(img_resize)
				img_resize = enhancer.enhance(0.6)

			img_resize.save(img_path)


def junk_del():
	shutil.rmtree(os.path.join(bgimage_dir))
	shutil.rmtree(bgm_dir)
	#shutil.rmtree(os.path.join(sound_dir,'seira'))
	shutil.rmtree(os.path.join(same_hierarchy,'data','scenario'))
	shutil.rmtree(os.path.join(same_hierarchy,'data','system'))
	shutil.rmtree(os.path.join(same_hierarchy,'data','video'))
	pass

text_cnv()
bgm_cnv()
music_cnv()
junk_del()