import faust

app = faust.App(
    'hello-world',
    broker='kafka://kafka:9092',
    value_serializer='raw',
    autodiscover=False
)

greetings_topic = app.topic('greetings')

@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)

if __name__ == '__main__':
    app.main()