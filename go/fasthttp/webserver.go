package main

import (
	"fmt"

	"github.com/valyala/fasthttp"
)

func handleHello(ctx *fasthttp.RequestCtx) {
	fmt.Fprint(ctx, "Hello World")
}

func main() {
	requestHandler := func(ctx *fasthttp.RequestCtx) {
		switch string(ctx.Path()) {
		case "/hello":
			handleHello(ctx)
		default:
			ctx.Error("Unsupported path", fasthttp.StatusNotFound)
		}
	}
	fmt.Println("=== server running on 127.0.0.1:8080 ===")
	fmt.Println("begin benchmark")
	fasthttp.ListenAndServe(":8080", requestHandler)
}
