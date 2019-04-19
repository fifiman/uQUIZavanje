CREATE TABLE `Users` (
`Id` int(11) NOT NULL AUTO_INCREMENT,
`Username` int(11) NOT NULL,
`Password` int(11) NOT NULL,
`Ranking` int(11) NULL,
`Picture` varchar(255) NOT NULL,
`Privileges` varchar(255) NULL,
`Banned` tinyint(1) NULL,
PRIMARY KEY (`Id`) 
);
CREATE TABLE `Friendships` (
`Id_first` int(11) NOT NULL,
`Id_second` int(11) NOT NULL,
PRIMARY KEY (`Id_first`, `Id_second`) 
);
CREATE TABLE `Games` (
`Id` int(11) NOT NULL,
`Id_player_one` int(11) NOT NULL,
`Id_player_two` int(11) NOT NULL,
`Id_player_three` int(11) NULL,
`Id_player_four` int(11) NULL,
`Player_one_pts` int(11) NOT NULL,
`Player_two_pts` int(11) NOT NULL,
`Player_three_pts` int(11) NULL,
`Player_four_pts` int(11) NULL,
PRIMARY KEY (`Id`) 
);
CREATE TABLE `Questions` (
`Id` int(11) NOT NULL,
`Text` varchar(255) NOT NULL,
`Answer_one` varchar(255) NOT NULL,
`Answer_two` varchar(255) NOT NULL,
`Answer_three` varchar(255) NOT NULL,
`Answer_four` varchar(255) NOT NULL,
`Correct` integer(11) NOT NULL,
`Category` varchar(255) NOT NULL,
PRIMARY KEY (`Id`) 
);

ALTER TABLE `Users` ADD CONSTRAINT `fk_Users_Friendships_1` FOREIGN KEY (`Id`) REFERENCES `Friendships` (`Id_first`);
ALTER TABLE `Users` ADD CONSTRAINT `fk_Users_Friendships_2` FOREIGN KEY (`Id`) REFERENCES `Friendships` (`Id_second`);
ALTER TABLE `Users` ADD CONSTRAINT `fk_Users_Games_1` FOREIGN KEY (`Id`) REFERENCES `Games` (`Id_player_one`);
ALTER TABLE `Users` ADD CONSTRAINT `fk_Users_Games_2` FOREIGN KEY (`Id`) REFERENCES `Games` (`Id_player_two`);
ALTER TABLE `Users` ADD CONSTRAINT `fk_Users_Games_3` FOREIGN KEY (`Id`) REFERENCES `Games` (`Id_player_three`);
ALTER TABLE `Users` ADD CONSTRAINT `fk_Users_Games_4` FOREIGN KEY (`Id`) REFERENCES `Games` (`Id_player_four`);

