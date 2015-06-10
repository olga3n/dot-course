#!/usr/bin/env escript
%% -*- erlang -*-
%%! -smp enable -name second@127.0.0.1 -setcookie random

main(_) ->
	Listener = 'first@127.0.0.1',

	io:format("~n-name ~s~n", [node()]),

	erlang:set_cookie(node(),'random'),
	io:format("-setcookie ~s~n~n", [erlang:get_cookie()] ),

	net_kernel:connect(Listener),
	io:fwrite("nodes: "),
	io:write(nodes()),
	io:fwrite("\n\n"),

	{distributor, Listener} ! {self(), ls},

	receive
		X -> io:fwrite(X);
		error -> exit(1)
	after 10000 -> exit(1)
	end,

	Name = string:strip(io:get_line("enter filename: "), right, $\n),
	io:fwrite("\n"),
	
	{distributor, Listener} ! {self(), {cat, Name}},
	
	receive
		{ok, L} -> io:fwrite(L);
		{error, _} -> exit(1)
	end.