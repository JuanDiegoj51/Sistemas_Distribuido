const axios = require('axios');
const AWS = require('aws-sdk');

// Configura tus credenciales de AWS
AWS.config.update({
  accessKeyId: 'ACCESS_KEY', 
  secretAccessKey: 'SECRET_ACCESS_KEY', 
  region: 'us-east-2' 
});

// Instancia del servicio SQS
const sqs = new AWS.SQS({ apiVersion: '2012-11-05' });

// URL de la cola SQS
const queueUrl = 'URL';  

// Función para enviar un número a SQS
async function sendNumberToSQS(number) {
  const params = {
    MessageBody: JSON.stringify({ number: number }),  // El número que enviamos a SQS
    QueueUrl: queueUrl
  };

  try {
    const data = await sqs.sendMessage(params).promise();
    console.log(`Mensaje enviado correctamente. ID del mensaje: ${data.MessageId}`);
  } catch (err) {
    console.error('Error enviando mensaje a SQS:', err);
  }
}

// Enviar números del 1 al 1,000,000 a SQS
for (let i = 1; i <= 1000000; i++) {
  sendNumberToSQS(i);
}
