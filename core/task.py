# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from core import schedule2
from apps.administracion.estadisticas.models import registroConectados
from apps.player.models import Player, Guild
from django.utils import timezone
from datetime import timedelta
from apps.varios.models import Top
from django.db import connections

def ha():

    now = timezone.now()
    #count = Player.objects.all().filter(last_play__range=[now - timedelta(minutes=55), now]).count()
    cursor = connections['player'].cursor()
    cursor.execute("SELECT COUNT(*) as count FROM player WHERE DATE_SUB(NOW(), INTERVAL 55 MINUTE) < last_play")
    a = cursor.fetchall()
    b = a[0][0]
    registroConectados(time=now, count=b).save()

    """def getLastIdTop():
        try:
            last_id = Top.objects.values('id').last()['id']
            return last_id
        except Top.DoesNotExist:
            return 0 """

    Top.objects.all().delete()
    b = Player.objects.all().values('id', 'account_id', 'name', 'job', 'level', 'exp', 'ranking', 'ip')
    for i in b:
        a = Top()
        a.account_id = i['account_id']
        a.name = i['name']
        a.job = i['job']
        a.level = i['level']
        a.exp = i['exp']
        try:
            b = Guild.objects.get(id=i['id'])
            a.guild_name = b.name
        except Guild.DoesNotExist:
            pass
        a.ranking = i['ranking']
        a.ip = i['ip']
        a.save()

def run_task(funcion_principal, funcion_secundaria):
    funcion_principal.every(1).hours.at(0).do(funcion_secundaria)
    funcion_principal.run_continuously()


run_task(schedule2, ha)
