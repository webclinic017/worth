# worth
Simple trading and cash management bookkeeping system.

## Introduction

### Goal
Keep track of wealth at a collection of brokers and banks across a variety of asset classes.  Do it privately, without storing information on third party servers.

## Reasoning
Maybe this isn't so reasonable. Sure, I could have used something off-the-shelf or another open source project.  But, I wanted this to be simple and private.  I did not want my data stored on someone else's server.  Lastly, I wanted to have a code base I could customize easliy and add asset classes to.  All that being said I'll surely borrow and use other open source packages from time to time.

This also serves as one of those projects I use to learn new things between other projects.  It was not started after a build vs buy study, although I have looked around a bit, but rather as a fun project to both improve my engineering skills and provide tools for wealth management.  It is simple and sometimes that isn't stupid.

## Stack
Django + Postgres + Pandas
Trades are entered manually or via brokerage APIs. \
Market data comes from the yahoo API.

## PGP
One of my brokers allows me to download monthly statements via ftp.  They recently required those files to be PGP encrypted.  Some of my notes are [here](pgp.md).