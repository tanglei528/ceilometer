#! /bin/bash

LOG_FILE=/tmp/packaging.log
LOG_MESSAGE="Details in ${LOG_FILE}"

echo 'Starting packaging...'
[ -f '$LOG_FILE' ] && rm -f ${LOG_FILE}

#echo 'Prepare production local setting'
#if [ -f openstack_dashboard/local/local_settings.py ] ; then
#  mv -f openstack_dashboard/local/local_settings.py openstack_dashboard/local/local_settings.py.backup
#fi
#cp openstack_dashboard/local/local_settings.py.production openstack_dashboard/local/local_settings.py

#echo 'Clean old compressed data...'
#[ -d static/dashboard/ ] && rm -rf static/dashboard/
#if [ -d openstack_dashboard/static/dashboard/css ] ; then
#  rm -rf openstack_dashboard/static/dashboard/css
#fi
#if [ -d openstack_dashboard/static/dashboard/js ] ; then
#  rm -rf openstack_dashboard/static/dashboard/js
#fi
#echo 'Compress js, less, etc...'
#tools/with_venv.sh ./manage.py compress > ${LOG_FILE} 2>&1
#if [ $? -ne 0 ]; then
#  echo "Error: compress failed. ${LOG_MESSAGE}"
#  exit 1
#fi
#cp -f static/dashboard/manifest.json openstack_dashboard/static/dashboard/manifest.json
#cp -rf static/dashboard/css/ openstack_dashboard/static/dashboard/
#cp -rf static/dashboard/js/ openstack_dashboard/static/dashboard/

echo 'Pack alarm...'
echo 'Prepare setup.cfg'
cp -f setup-ceilometer-alarm.cfg setup.cfg
echo 'Build rpm package...'
python setup.py bdist_rpm >> ${LOG_FILE} 2>&1
if [ $? -ne 0 ]; then
  echo "Error: build alarm rpm package failed. ${LOG_MESSAGE}"
  exit 1
fi

echo 'Pack api...'
mv -f setup.cfg setup.cfg.bak
echo 'Prepare setup.cfg'
cp -f setup-ceilometer-api.cfg setup.cfg
echo 'Build rpm package...'
python setup.py bdist_rpm >> ${LOG_FILE} 2>&1
if [ $? -ne 0 ]; then
  echo "Error: build api rpm package failed. ${LOG_MESSAGE}"
  exit 1
fi


echo 'Pack central...'
echo 'Prepare setup.cfg'
cp -f setup-ceilometer-central.cfg setup.cfg
echo 'Build rpm package...'
python setup.py bdist_rpm >> ${LOG_FILE} 2>&1
if [ $? -ne 0 ]; then
  echo "Error: build central rpm package failed. ${LOG_MESSAGE}"
  exit 1
fi

echo 'Pack collector...'
echo 'Prepare setup.cfg'
cp -f setup-ceilometer-collector.cfg setup.cfg
echo 'Build rpm package...'
python setup.py bdist_rpm >> ${LOG_FILE} 2>&1
if [ $? -ne 0 ]; then
  echo "Error: build collector rpm package failed. ${LOG_MESSAGE}"
  exit 1
fi

echo 'Pack compute...'
echo 'Prepare setup.cfg'
cp -f setup-ceilometer-compute.cfg setup.cfg
echo 'Build rpm package...'
python setup.py bdist_rpm >> ${LOG_FILE} 2>&1
if [ $? -ne 0 ]; then
  echo "Error: build compute rpm package failed. ${LOG_MESSAGE}"
  exit 1
fi

echo 'Pack notification...'
echo 'Prepare setup.cfg'
cp -f setup-ceilometer-notification.cfg setup.cfg
echo 'Build rpm package...'
python setup.py bdist_rpm >> ${LOG_FILE} 2>&1
if [ $? -ne 0 ]; then
  echo "Error: build notification rpm package failed. ${LOG_MESSAGE}"
  exit 1
fi
#echo 'Pack successfully, rpm packages are in dist/ directory'
#mv -f setup.cfg.bak setup.cfg
#mv -f openstack_dashboard/local/local_settings.py.backup openstack_dashboard/local/local_settings.py
#rm -f openstack_dashboard/static/dashboard/manifest.json
#rm -rf openstack_dashboard/static/dashboard/css
#rm -rf openstack_dashboard/static/dashboard/js

mv setup.cfg.bak setup.cfg
exit 0
