#!/bin/bash
# Copy a site's contents from another server after deploying it via fab
WWWDIR=/var/www
CONTENTDIRS="backup photologue medialibrary"
OLDSERVER=$1
SITE=$2

if [ "$SITE" == "" ]; then
  echo "Usage: $0 source_server site_name"
  exit 1
fi

for CDIR in $CONTENTDIRS
do
  echo "SCP tries to copy $CDIR from $OLDSERVER..."
  scp -pr root@$OLDSERVER:$WWWDIR/$SITE/$CDIR $WWWDIR/$SITE/
  chown -R $SITE:$SITE $WWWDIR/$SITE/$CDIR
done

gunzip `ls -t $WWWDIR/$SITE/backup/*.sql.gz | head -1`
SQL=`ls -t $WWWDIR/$SITE/backup/*.sql | head -1`
echo "Importing data from $SQL as user $SITE..."
mysql -u $SITE -p -D $SITE < $SQL
