pipeline {
    agent none 
    stages {
        stage('Set up') {
            agent { dockerfile true } 
            steps {
                withCredentials([string(credentialsId: 'vault-root-token', variable: 'RTOKEN'),usernamePassword(credentialsId: 'patoken', passwordVariable: 'password', usernameVariable: 'username')]){
                 sh 'echo $RTOKEN'
                 sh 'python -V'
                 sh 'python /root/python.py $password $RTOKEN'
               }
             
            }
        }
    }
}
