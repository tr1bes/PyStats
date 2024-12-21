// ############################################################################################
// PyStats using Bov's DLL

// This allows Tribes server related events to be stream-lined to a python socket
// that is connected to the listening port on the server. The listener will repeatedly run
// and listen for events 0.1 seconds. Any changes made in the actual 'code.pystats.cs' 
// script will automatically reflect on the python script once re-executed in the console.
//
// You now have the ability to manipulate the data outside of the game how you wish.
//
// Big thank you to Bovidi for allowing this to happen!
//
// ############################################################################################

$PyStats::Version = "1.0";

// #####################################################
// # Variables
// #####################################################

$PyStats::ConnectionCreated = false; // Keep track of a connection
$PyStats::EnableServerDebug = false; // Enables server debugging (Warning: Super annoying..)
$PyStats::EnableDamageDebug = false; // Enables damage results

$PyStats::Enabled = true; // Run PyStats (Default: True)
$PyStats::ListeningPort = "28011"; // The port python should listen to


// Do not run if not enabled
if(!$PyStats::Enabled)
	return;


function PyStats::Init()
{	
	if(Bov::createConnection($PyStats::ListeningPort) && !$PyStats::ConnectionCreated) {
		$PyStats::ConnectionCreated = true;
		echo("*** PyStats Running ", $PyStats::Version, " ***");
		echo("***   -> Local Port: ", $PyStats::ListeningPort);
	}
	
	Bov::Broadcast(
		sprintf("START: %1 %2", $missionname, timestamp())
	);
}
Attachment::AddAfter("Game::startMatch", "PyStats::Init");

// #####################################################
// # 					Client Events                  #
// #####################################################

function PyStats::onDamage(%this, %type, %value, %pos, %vec, %mom, %vertPos, %quadrant, %object) 
{
	if(!$PyStats::EnableDamageDebug)
		return;
	
	if(%object != 0) {
		Bov::Broadcast(
			sprintf("DMG: ID: %1 (%2), %3, %4", %object, Client::GetName(%object), %value, %quadrant)
		);
	}
}
Attachment::AddAfter("Player::onDamage", "PyStats::onDamage");

function PyStats::onKilled(%playerId, %killerId, %damageType)
{
	%killMsg = %score = "";

	if(%playerId == %killerId) {
		%score = floor(%playerId.score);
		%killMsg = sprintf("SUICIDE: ID: %1 (%2) = Score %3", %playerId, Client::GetName(%playerId), %score);
	} else {
		%score = floor(%killerId.score);
		%killMsg = sprintf("PLAYER: ID: %1 (%2) killed (%3) %4 = Score %5", %killerId, Client::GetName(%killerId), %playerId, Client::GetName(%playerId), %score);
	}
			
	Bov::Broadcast(%killMsg);
}
Attachment::AddAfter("Client::onKilled", "PyStats::onKilled");

function PyStats::ServerMessage(%mtype, %message, %filter)
{
    if($PyStats::EnableServerDebug) {
		Bov::Broadcast(
			sprintf("SERVER: %1 %2", %message, %filter)
		);
	}
}
Attachment::AddAfter("messageAll", "PyStats::ServerMessage");
Attachment::AddAfter("messageAllExcept", "PyStats::ServerMessage");

function PyStats::Say(%clientId, %team, %message)
{
    Bov::Broadcast(
		sprintf("SAY: ID: %1 %2 %3", %clientId, %team, %message)
	);
}
Attachment::AddAfter("remoteSay", "PyStats::Say");

function PyStats::playerSpawned(%pl, %clientId, %armor) 
{
    %team = getTeamName(Client::GetTeam(%clientId));
    Bov::Broadcast(
		sprintf("SPAWN: ID: %1 (%2) spawns on %3", %clientId, Client::GetName(%clientId), %team)
	);
}
Attachment::AddAfter("Game::playerSpawned", "PyStats::playerSpawned");

function PyStats::onServerConnect(%clientId) 
{
    Bov::Broadcast(
		sprintf("CONNECT: ID: %1 (%2)", %clientId, Client::GetName(%clientId))
	);
}
Attachment::AddAfter("Server::onClientConnect", "PyStats::onServerConnect");

function PyStats::leaveGame(%clientId)
{
	Bov::Broadcast(
		sprintf("BYE: ID: %1 (%2)", %clientId, Client::GetName(%clientId))
	);
}
Attachment::AddAfter("Client::leaveGame", "PyStats::leaveGame");


// #####################################################
// # 					Flag Events					   #
// #####################################################

function PyStats::onFlagGrab(%team, %cl)
{
	if(%cl == 0)
		return;
	
	Bov::Broadcast(
		sprintf("FLAG: %1 (%2) grabbed the %3 flag", %cl, Client::GetName(%cl), getTeamName(%team))
	);
}
Attachment::AddAfter("Client::onFlagGrab", "PyStats::onFlagGrab");

function PyStats::onFlagPickup(%team, %cl)
{
	if(%cl == 0)
		return;
	
	Bov::Broadcast(
		sprintf("FLAG: %1 (%2) picked up the %3 flag", %cl, Client::GetName(%cl), getTeamName(%team))
	);
}
Attachment::AddAfter("Client::onFlagPickup", "PyStats::onFlagPickup");

function PyStats::onFlagCap(%team, %cl)
{
	if(%cl == 0)
		return;
	
	Bov::Broadcast(
		sprintf("FLAG: ID: %1 (%2) capped the %3 flag", %cl, Client::GetName(%cl), getTeamName(%team))
	);
}
Attachment::AddAfter("Client::onFlagCap", "PyStats::onFlagCap");

function PyStats::onFlagReturn(%team, %cl)
{
	if(%cl == 0)
		return;
	
	Bov::Broadcast(
		sprintf("FLAG: %1 (%2) returned the %3 flag", %cl, Client::GetName(%cl), getTeamName(%team))
	);
}
Attachment::AddAfter("Client::onFlagReturn", "PyStats::onFlagReturn");

function PyStats::onFlagDrop(%team, %cl)
{
	if(%cl == 0)
		return;
	
	Bov::Broadcast(
		sprintf("FLAG: %1 (%2) dropped the %3 flag", %cl, Client::GetName(%cl), getTeamName(%team))
	);
}
Attachment::AddAfter("Client::onFlagDrop", "PyStats::onFlagDrop");

function PyStats::flagleaveMissionArea(%this, %playerId) 
{
    Bov::Broadcast(
		sprintf("FLAG: ID: %1 (%2) left the mission area with the flag.", %playerId, Client::GetName(%playerId))
	);
}
Attachment::AddAfter("Flag::leaveMissionArea", "PyStats::flagleaveMissionArea");

PyStats::Init();
