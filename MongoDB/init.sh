mongo <<EOF
    use users_service
    db.users.createIndex({username: 1}, {unique: true})
    db.createUser({user: 'users_service', pwd: 'users_service_pwd', roles: [ 'readWrite' ]})
    db.users.insertOne({first_name: 'Set', last_name: 'Name', username: 'admin', password: '\$2b\$12\$F7PwlicCMaEIHlb0MbVMG.WSeizpUg5M1scloPR039DtNCu0.9qKO', admin: true})
    db.users.insertOne({first_name: '', last_name: '', username: 'scheduling_service', password: '\$2b\$12\$F7PwlicCMaEIHlb0MbVMG.WSeizpUg5M1scloPR039DtNCu0.9qKO', admin: false})
EOF
