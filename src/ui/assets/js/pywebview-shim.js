window.pywebview = {
    api: new Proxy({}, {
        get(target, methodName) {
            return function (...args) {
                return fetch('/api/rpc', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ method: methodName, args })
                })
                    .then((resp) => resp.json())
                    .then((data) => {
                        if (data && data.error) throw new Error(data.error);
                        return data ? data.result : undefined;
                    });
            };
        }
    })
};
