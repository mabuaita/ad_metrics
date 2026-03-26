# About The Project

This is a ad metric that injests mobile devices ad research metrics and make them available to subsequent processes.

# Getting Started

You need an api key from openweathermap, it's free unless you exceed the quota. Store the key in the ".env" file, it gets consumed by the app.

**Installation**

This app can be run be run in a container or locally, a requirements.txt file is included. If you run it in your dev environment make sure you activate your venv  virtual environment.

All that's needed is to clone this repository.

# Features

- Uses develop branch to track development, when a release is ready a merge to main/master is requested.
- Developers use feature branches or bug-fix branches, which can be merged beck to develop branch.
- For merge requests a jenkins job automaticlly initiates to test for untime resilience and framework mechanics.
- Merge to main only if test job passes and peer review.
- Instrumented to render metrics for prometheus to scape, http://ad-metrics.swhagy.com:8777/metrics.
- Health checker, http://ad-metrics.swhagy.com:8777/health.
- Graceful shutdown, http://ad-metrics.swhagy.com:8777/shutdown.
- Log collection via Loki, uses structured logging (key/value pairs) for better usability: formatter = jsonlogger.JsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')

# Roadmap

- Phase out jenkins and use gitaction instead.
- Use external metrics, such as those from prometheus, to automatically scale the pods.
- Add automated load test for each merge request, at the moment it's manual.
- Implement more advanced configuration management, using tiered service levels, allowing for more frequent promethues scraping and tighter alerts threshold for higher level applications.

# Availability/scalability

- The app runs on a k8s with elastic deployment that will scale up to 10 replicas, based on cpu usage. It is also configured to use multiple availablitiy zones.
- The data is kept on S3, with version control and replication.
- Istio is enabled for better recovery.

========================================================================================

# prometheus.yml

**global:**

    scrape_interval: 15s
    scrape_timeout: 10s
    evaluation_interval: 15s

**scrape_configs:**

  Self-monitoring

    - job_name: 'prometheus'
      static_configs:
    - targets: ['localhost:9090']

  Application servers grouped by service

     - job_name: 'api-gateway'
      static_configs:
      - targets:
          - 'http://ad-metrics.swhagy.com:8777'
        labels:
          service: 'weather-app'
          tier: 'frontend'

  **---------------------------------------------------------------------------------------------------**

# Alertmanager Routing

**route:**

    receiver: default
    group-by: [alertname, service]
    group-wait: 30s
    group-interval: 5m
    repeat-interval: 4h

**routes:**
    # Critical production alerts page immediately, warnings create tickets
    
    - match:
        severity: critical
        environment: production
      receiver: pagerduty
      continue: true

    # Also send to Slack for visibility
    - match:
        severity: critical
      receiver: slack-critical

    # Warnings create tickets
    - match:
        severity: warning
      receiver: ticketing-system
      group-wait: 10m

**receivers:**
  .
  - name: default
    slack-configs:
      - channel: '#alerts'
  - name: pagerduty
    pagerduty_configs:
      - service_key: 'your-pagerduty-key'
  - name: slack-critical
    slack-configs:
      - channel: '#incidents'
  - name: ticketing-system
    webhook_configs:
      - url: https://tickets.example.com/webhook
  .

      **----------------------------------------------------------------------------------------------------------**

# Observability

In the code we instrumented the app to create two metrics: a Counter that tracks the total number of HTTP requests
(with labels for method, endpoint, and status code), and a Histogram that measures request duration.
The /metrics endpoint returns all metrics in Prometheus format using the generate_latest() function.
The code measures how long it takes to process the request then records the duration in the histogram using the .observe() method
and increments the request counter using .inc(). The labels allow you to filter and aggregate metrics in your Prometheus queries.

`# Start timer

    start_time = time.time()
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    response = cityweather(city)

    duration = time.time() - start_time
    REQUEST_LATENCY.labels(method='GET', endpoint='/').observe(duration)
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=200).inc()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=400).inc()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=404).inc()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=500).inc()
    REQUEST_COUNT.labels(method='GET', endpoint='/', status=503).inc()`

From above we're able to calculate Latency, Requests per Second (Rate), Error rates, and Irate:
# Endpoint Metric Definition
| Metric.       | Description                                                                                                    |
| ------------- | -------------------------------------------------------------------------------------------------------------- |
|  Latency      |    The median 50th (P50) and 99th percentile (P99) round-trip latency times.                                   |    
|  Errors/Sec   |    The number of errors (4xx and 5xx) processed per second. 5xx garners higher attension over 4xx, for good SLO|
|  Rate()       |    The number of requests processed per second.                                                                |
|  Irate()      |    Instantaneous per-second rate of change.                                                                    |

* rate() averages no. of request over the scraping period, giving a trend that helps plan capacity.
** irate() is burstable in nature and is instrumental in expaling what is happening in the moment.

**Other things we'd like to monitor**
   
| Metric          | Description |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------  |
| Service Uptime  | We don't just monitor SLI but SLO monitoring entails we monitor service uptime, if business requires 99.995 uptime, we adhere to the metric.|
| CPU Usage %     | Average CPU usage.                                                                                                                          |
| Memory Usage %. | Average memory usage.                                                                                                                       |
| Concurrency.    | The maximum number of parallel requests that the system can handle. Provisioned concurrency dynamically adjusts within the minimum and maximum limits of the compute scale-out range, varying in response to incoming traffic.|
