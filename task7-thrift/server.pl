#!/usr/bin/env perl

use strict;

use Thrift::Socket;
use Thrift::Server;

use lib 'gen-perl';
use lib 'gen-perl/parser';

use LWP::Simple;

package ParserHandler;

use Parser;
use base qw/parser::ParserIf/;

sub new()
{
	my $class = shift;
	my $self = {};

	return bless($self, $class);
}

sub get_domains($$)
{
	my @l;
	my ($self, $url) = @_;

	if ($url) {
		$_ = LWP::Simple::get($url);

		s/<!\-\-.*?\-\->/ /sg;
		
		s#<\s*script.*?<\s*/\s*script\s*># #isg;
		s#<\s*style.*?<\s*/\s*style\s*># #isg;

		@l = ( $_ =~ /.*<\s*a\s*href\=.?https?\:\/\/([^\s\/\?"']+).*/img );
	}

	my %t = map { $_ => 1 } @l;
	
	@l = keys %t;

	print $url, " ", ($#l + 1), "\n";

	return (join "\n", @l);
}

eval {

	my $handler = new ParserHandler;
	my $processor = new parser::ParserProcessor($handler);
	my $socket = new Thrift::ServerSocket(12345);
	my $server = new Thrift::ForkingServer($processor, $socket);

	print "listen...\n";

	$server -> serve;
}
