#!/usr/bin/env escript
%% -*- erlang -*-
%%! -smp enable -name first@127.0.0.1 -setcookie random 

-module(dist).
-include_lib("kernel/include/file.hrl").

-export([main/1]).

get_listing(_, []) -> "";
get_listing(Pref, [H|T]) ->
	Name = Pref ++ "/" ++ H,
	case file:read_file_info(Name) of
		{ok, Info} ->
			{{Year, Month, Day}, {Hour, Min, Sec}} = Info#file_info.mtime,
			I = io_lib:format(
				"~.8B\t~p\t~2..0B-~2..0B-~4B ~2..0B:~2..0B:~2..0B\t~s~n", 
				[
					Info#file_info.mode band 8#777, 
					Info#file_info.size,
					Month, Day, Year, Hour, Min, Sec,
					H
				]),
			
			get_listing(Pref, T) ++ I
	end.

read_text(H) ->
	case file:read_line(H) of
		{ok, Line} ->
			[Line] ++ read_text(H);
		eof -> []
	end.

cmd("ls", X) ->
	case file:list_dir_all(X) of
		{ok, Lst} ->
			io_lib:format("~s~n", [get_listing(X, Lst)]);
		{error, _} -> error
	end;
cmd("cat", X) ->
	case file:open(X, [read]) of
		{ok, H} -> 
			R = read_text(H),
			file:close(H),
			{ok, io_lib:format("~s~n", [R])};
		{error, M} -> {error, M}
	end;
cmd(_, _) ->
	io_lib:format("No such command.~n"),
	error.

cmd("ls") -> cmd("ls", ".");
cmd(_) ->
	io_lib:format("No such command.~n"),
	error.

listen() ->
	receive
		{Id, ls} -> 
			io:format("client: ~p; command: ls~n", [Id]),
			
			Id ! cmd("ls"),
			listen();

		{Id, {cat, X}} -> 
			io:format("client: ~p; command: cat ~s~n", [Id, X]),

			Id ! cmd("cat", X),
			listen();

		{Id, _} ->
			Id ! error, 
			listen();

		_ ->
			listen()

	after infinity -> ok
	end.

main(_) ->
	io:format("~n-name ~s~n", [node()]),

	erlang:set_cookie(node(),'random'),
	io:format("-setcookie ~s~n~n", [erlang:get_cookie()] ),
	
	Pid = spawn(fun() -> listen() end),
	register(distributor, Pid),

	io:format("distributor PID: ~p~n", [Pid]),
	
	%io:write(registered()),
	%io:fwrite("\n"),
	%user_drv:start(),

	timer:sleep(infinity),
	ok.