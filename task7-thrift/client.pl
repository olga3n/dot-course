#!/usr/bin/env perl

use strict;

use Thrift;
use Thrift::Socket;
use Thrift::BinaryProtocol;
use Thrift::BufferedTransport;

use lib 'gen-perl';
use lib 'gen-perl/parser';
use Parser;

my $socket = new Thrift::Socket('localhost', 12345);
my $transport = new Thrift::BufferedTransport($socket, 1024, 1024);
my $protocol = new Thrift::BinaryProtocol($transport);

my $client = new parser::ParserClient($protocol);

$, = "\n";

eval {
	$transport -> open();

	my %h;

	open f, "urls.txt" or die "Oops.\n";

	while (<f>){
		my $url = $_;
		
		chomp $url;

		my @l = split "\n", $client -> get_domains($url);
		
		for (@l) { $h{$_}++ };

		print @l, "\n";

	}

	close f;

	my @sorted_urls = sort { $h{$b} <=> $h{$a} } keys %h;

	foreach my $url ( @sorted_urls ) {
		print "$url $h{$url}\n";
	}

	print "\n\n";	

	my $i;
	while( $h{$sorted_urls[$i]} == $h{$sorted_urls[0]} )
	{
		print $sorted_urls[$i]."\n";
		$i++;
	}

	$transport -> close();
}

