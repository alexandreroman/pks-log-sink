# PKS Log Sink Demo

This demo project shows how to route logs from pods running in a Kubernetes cluster
created by [PKS](https://pivotal.io/platform/pivotal-container-service).

In this project, we use
[Papertrail](https://papertrailapp.com) as a remote syslog server, but you
are free to use any syslog server (even one running within your cluster).

## How to use it?

### Configuring the log router

Create a [Papertrail](https://papertrailapp.com) account: it's free.

Write down the Papertrail syslog remote server address & port
shown in the page [Setup Logging](https://papertrailapp.com/systems/setup?type=system&platform=unix).
Set these values as environment variables:
```shell
$ SYSLOG_SERVER=logsX.papertrailapp.com
$ SYSLOG_PORT=XXXXX
```

Store these credentials as Kubernetes secrets:
```shell
$ kubectl create secret generic syslog-destination --from-literal=syslog-destination=syslog+tls://$SYSLOG_SERVER:$SYSLOG_PORT
```

Papertrail configuration is done: you are now ready to route logs.

### Starting demo app

Install this demo app to your cluster:
```shell
$ kubectl apply -f pks-log-sink.yml
```

A new pod named `pks-log-sink` is installed in the namespace `pks-log-sink`.
This pod is exposed through a `LoadBalancer` on port `80`.
Each received HTTP request is logged: all log entries are then routed to
the remote syslog server.

An other pod named `syslog-router` is also running.
This pod is responsible for routing all log entries to the remote
syslog server. Since we just set Papertrail destination in our Kubernetes secrets,
this router will send these logs to this remote server.

Get the allocated public IP address for the app (look at `EXTERNAL_IP`):
```shell
$ kubectl get services --namespace pks-log-sink
NAME              TYPE           CLUSTER-IP       EXTERNAL-IP      PORT(S)        AGE
pks-log-sink-lb   LoadBalancer   10.100.200.162   35.241.139.108   80:31873/TCP   59s
```

Using your browser, navigate to this IP address.
A log entry should have been sent to Papertrail.

### Displaying logs in Papertrail

Go to the [Papertrail Dashboard](https://papertrailapp.com/dashboard).
You should see many systems, corresponding to Kubernetes pods.
Click on `pks-log-sink`.
<img src="https://imgur.com/download/5E19rGl"/>

You should see log entries received from the namespace `pks-log-sink`:
<img src="https://imgur.com/download/OTckD4k"/>

## Contribute

Contributions are always welcome!

Feel free to open issues & send PR.

## License

Copyright &copy; 2018 Pivotal Software, Inc.

This project is licensed under the [Apache Software License version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
