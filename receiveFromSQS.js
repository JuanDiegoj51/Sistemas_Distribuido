const AWS = require('aws-sdk');

// Configurar las credenciales de AWS
AWS.config.update({
    region: 'us-east-2',
    accessKeyId: '',  // 
    secretAccessKey: ''
});

// Instancia del servicio SQS
const sqs = new AWS.SQS({ apiVersion: '2012-11-05' });

// URL de la cola SQS
const queueUrl = '';

// Contador para rastrear el tiempo sin mensajes
let noMessageCount = 0; // Contador de segundos sin recibir mensajes

// Función para recibir y procesar mensajes de SQS
const receiveMessages = async () => {
    const params = {
        QueueUrl: queueUrl,
        MaxNumberOfMessages: 10, // Puedes ajustar esto
        WaitTimeSeconds: 20 // Long polling
    };

    try {
        const data = await sqs.receiveMessage(params).promise();
        if (data.Messages) {
            for (const message of data.Messages) {
                const number = JSON.parse(message.Body).number;
                console.log(`Número recibido: ${number}`);
                
                // Aquí puedes realizar cálculos o almacenar en la base de datos

                // Eliminar el mensaje de la cola después de procesarlo
                await sqs.deleteMessage({
                    QueueUrl: queueUrl,
                    ReceiptHandle: message.ReceiptHandle
                }).promise();
                console.log(`Mensaje eliminado: ${message.MessageId}`);

                // Reiniciar el contador si se recibe un mensaje
                noMessageCount = 0; 
            }
        } else {
            // Incrementar el contador si no hay mensajes
            noMessageCount++;
        }
    } catch (err) {
        console.error('Error al recibir mensajes:', err);
    }
};

// Función para mostrar un mensaje si no se han recibido solicitudes
const checkForMessages = () => {
    if (noMessageCount > 0) {
        console.log(`No se ha recibido ninguna solicitud en ${noMessageCount} segundo(s)`);
    }
};

// Iniciar la recepción de mensajes
setInterval(() => {
    receiveMessages();
    checkForMessages();
}, 1000); // Intervalo de 1 segundo
